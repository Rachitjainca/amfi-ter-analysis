"""
AMFI TER Analysis for GitHub Actions
Runs daily to compare TER changes and generate reports
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ter_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
Path('downloads').mkdir(exist_ok=True)
Path('output').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)
Path('history').mkdir(exist_ok=True)

# File paths
STATE_FILE = 'ter_state.json'
API_URL = 'https://www.amfiindia.com/api/populate-te-rdata-revised'

def load_state():
    """Load state from JSON file and validate/migrate schema"""
    default_state = get_default_state()
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                loaded_state = json.load(f)
            
            # Validate and migrate state structure
            # Ensure all required keys exist
            for key in default_state.keys():
                if key not in loaded_state:
                    logger.info(f"Missing key '{key}' in state, using default value")
                    loaded_state[key] = default_state[key]
            
            # Handle old format migration (last_month/last_year -> month_year)
            if 'month_year' not in loaded_state and 'last_year' in loaded_state and 'last_month' in loaded_state:
                loaded_state['month_year'] = f"{loaded_state['last_year']}-{loaded_state['last_month']:02d}"
                logger.info(f"Migrated old state format to new format: month_year={loaded_state['month_year']}")
            
            return loaded_state
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            return default_state
    return default_state

def get_default_state():
    """Get default state structure"""
    today = datetime.now().date()
    return {
        'last_processed_date': str(today),
        'month_year': f"{today.year}-{today.month:02d}",
        'file_history': {},
        'daily_snapshots': {}
    }

def save_state(state):
    """Save state to JSON file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        logger.info("State saved successfully")
    except Exception as e:
        logger.error(f"Error saving state: {e}")

def download_ter_file(year, month):
    """Download TER file from AMFI API"""
    try:
        logger.info(f"Downloading TER file for {year}-{month:02d}...")
        
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        
        # Save to downloads folder with timestamp
        filename = f"downloads/TER_{year}_{month:02d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Downloaded: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error downloading TER file: {e}")
        return None

def read_ter_file(filepath):
    """Read TER file and return dataframe"""
    try:
        df = pd.read_excel(filepath)
        logger.info(f"Read {len(df)} records from {filepath}")
        return df
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}")
        return None

def get_latest_file_for_month(year, month):
    """Get the latest downloaded file for a specific month"""
    downloads_dir = Path('downloads')
    pattern = f"TER_{year}_{month:02d}_*.xlsx"
    
    files = list(downloads_dir.glob(pattern))
    if files:
        # Return the most recent file
        return str(max(files, key=lambda p: p.stat().st_mtime))
    return None

def compare_schemes(old_df, new_df, plan_type):
    """Compare two dataframes and return changes"""
    try:
        # Use NSDL Scheme Code as unique identifier
        old_df = old_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        new_df = new_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        
        # Column name depends on plan type
        if plan_type == 'Regular':
            ter_col = 'Regular Plan - Base TER (%)'
        else:
            ter_col = 'Direct Plan - Base TER (%)'
        
        # Merge on scheme code
        merged = pd.merge(
            old_df[['NSDL Scheme Code', 'Scheme Name', ter_col]],
            new_df[['NSDL Scheme Code', 'Scheme Name', ter_col]],
            on='NSDL Scheme Code',
            suffixes=('_old', '_new')
        )
        
        # Calculate change (positive = TER reduction)
        merged['TER Reduction (%)'] = merged[f'{ter_col}_old'] - merged[f'{ter_col}_new']
        merged = merged[merged['TER Reduction (%)'] != 0].copy()  # Only changes
        
        # Rename and reorder columns
        merged = merged[[
            'NSDL Scheme Code',
            'Scheme Name_new',
            f'{ter_col}_old',
            f'{ter_col}_new',
            'TER Reduction (%)'
        ]]
        
        merged.columns = [
            'NSDL Scheme Code',
            'Scheme Name',
            'Old TER (%)',
            'New TER (%)',
            'TER Reduction (%)'
        ]
        
        return merged
    except Exception as e:
        logger.error(f"Error comparing schemes for {plan_type}: {e}")
        return pd.DataFrame()

def analyze_daily():
    """Main analysis function for daily execution"""
    logger.info("=" * 60)
    logger.info("Starting AMFI TER Analysis")
    logger.info("=" * 60)
    
    state = load_state()
    today = datetime.now().date()
    today_str = str(today)
    current_month_year = f"{today.year}-{today.month:02d}"
    
    logger.info(f"Current date: {today}")
    logger.info(f"Last processed: {state['last_processed_date']}")
    logger.info(f"Current month: {current_month_year}")
    
    # Check if month changed
    if state['month_year'] != current_month_year:
        logger.info("Month changed! Downloading new month's file...")
        
        # Download new month file
        filepath = download_ter_file(today.year, today.month)
        if filepath:
            df = read_ter_file(filepath)
            if df is not None:
                state['month_year'] = current_month_year
                state['last_processed_date'] = today_str
                
                # Save as baseline for the month
                state['file_history'][current_month_year] = {
                    'filepath': filepath,
                    'date': today_str
                }
                save_state(state)
                logger.info("New month baseline set. Waiting for next day comparison.")
        return
    
    # Same month - check if it's a new day
    if state['last_processed_date'] == today_str:
        logger.info("Already processed today. Skipping.")
        return
    
    # New day in same month - download and compare
    logger.info("New day detected. Downloading current month file...")
    
    current_filepath = download_ter_file(today.year, today.month)
    if not current_filepath:
        logger.error("Failed to download current file")
        return
    
    # Get baseline file for this month
    baseline_key = current_month_year
    if baseline_key not in state['file_history']:
        logger.warning(f"No baseline file found for {baseline_key}")
        return
    
    baseline_filepath = state['file_history'][baseline_key].get('filepath')
    if not baseline_filepath or not os.path.exists(baseline_filepath):
        logger.error(f"Baseline file not found: {baseline_filepath}")
        return
    
    # Read both files
    baseline_df = read_ter_file(baseline_filepath)
    current_df = read_ter_file(current_filepath)
    
    if baseline_df is None or current_df is None:
        logger.error("Failed to read data files")
        return
    
    # Compare Regular Plan
    logger.info("Comparing Regular Plan TER changes...")
    regular_changes = compare_schemes(baseline_df, current_df, 'Regular')
    
    if len(regular_changes) > 0:
        output_file = f"output/Regular_Plan_TER_Changes_{today}.csv"
        regular_changes.to_csv(output_file, index=False)
        logger.info(f"Regular Plan: {len(regular_changes)} changes found")
        logger.info(f"Saved to {output_file}")
    else:
        logger.info("Regular Plan: No changes found")
    
    # Compare Direct Plan
    logger.info("Comparing Direct Plan TER changes...")
    direct_changes = compare_schemes(baseline_df, current_df, 'Direct')
    
    if len(direct_changes) > 0:
        output_file = f"output/Direct_Plan_TER_Changes_{today}.csv"
        direct_changes.to_csv(output_file, index=False)
        logger.info(f"Direct Plan: {len(direct_changes)} changes found")
        logger.info(f"Saved to {output_file}")
    else:
        logger.info("Direct Plan: No changes found")
    
    # Generate comparison between Regular and Direct
    if len(regular_changes) > 0 and len(direct_changes) > 0:
        try:
            logger.info("Generating Regular vs Direct comparison...")
            
            # Merge on scheme name to find common schemes
            comparison = pd.merge(
                regular_changes[['Scheme Name', 'TER Reduction (%)']],
                direct_changes[['Scheme Name', 'TER Reduction (%)']],
                on='Scheme Name',
                suffixes=('_Regular', '_Direct')
            )
            
            if len(comparison) > 0:
                comparison['Difference (%)'] = comparison['TER Reduction (%)_Direct'] - comparison['TER Reduction (%)_Regular']
                output_file = f"output/Regular_vs_Direct_TER_Changes_{today}.csv"
                comparison.to_csv(output_file, index=False)
                logger.info(f"Regular vs Direct: {len(comparison)} common schemes with changes")
                logger.info(f"Saved to {output_file}")
        except Exception as e:
            logger.error(f"Error generating comparison: {e}")
    
    # Update state
    state['last_processed_date'] = today_str
    save_state(state)
    
    logger.info("=" * 60)
    logger.info("Analysis completed successfully")
    logger.info("=" * 60)

def generate_notification_data():
    """
    Generate detailed notification data with actual data from CSV files
    """
    summary = {
        'date': str(datetime.now().date()),
        'regular_count': 0,
        'direct_count': 0,
        'comparison_count': 0,
        'regular_changes': [],
        'direct_changes': [],
        'comparison_data': []
    }
    
    output_dir = Path('output')
    if output_dir.exists():
        # Read Regular Plan changes
        regular_file = list(output_dir.glob('Regular_Plan_TER_Changes_*.csv'))
        if regular_file:
            try:
                df = pd.read_csv(regular_file[0])
                summary['regular_count'] = len(df)
                # Get top 5 changes
                top_changes = df.nlargest(5, 'TER Reduction (%)')
                for idx, row in top_changes.iterrows():
                    summary['regular_changes'].append({
                        'scheme': row['Scheme Name'],
                        'old_ter': float(row['Old TER (%)']),
                        'new_ter': float(row['New TER (%)']),
                        'reduction': float(row['TER Reduction (%)'])
                    })
                logger.info(f"Regular Plan: {summary['regular_count']} changes")
            except Exception as e:
                logger.warning(f"Could not read Regular Plan file: {e}")
        
        # Read Direct Plan changes
        direct_file = list(output_dir.glob('Direct_Plan_TER_Changes_*.csv'))
        if direct_file:
            try:
                df = pd.read_csv(direct_file[0])
                summary['direct_count'] = len(df)
                # Get top 5 changes
                top_changes = df.nlargest(5, 'TER Reduction (%)')
                for idx, row in top_changes.iterrows():
                    summary['direct_changes'].append({
                        'scheme': row['Scheme Name'],
                        'old_ter': float(row['Old TER (%)']),
                        'new_ter': float(row['New TER (%)']),
                        'reduction': float(row['TER Reduction (%)'])
                    })
                logger.info(f"Direct Plan: {summary['direct_count']} changes")
            except Exception as e:
                logger.warning(f"Could not read Direct Plan file: {e}")
        
        # Read Comparison data
        comparison_file = list(output_dir.glob('*Regular_vs_Direct*.csv'))
        if comparison_file:
            try:
                df = pd.read_csv(comparison_file[0])
                summary['comparison_count'] = len(df)
                # Get top positive and negative differences
                top_differences = pd.concat([
                    df.nlargest(3, 'Difference (%)'),
                    df.nsmallest(3, 'Difference (%)')
                ]).drop_duplicates()
                
                for idx, row in top_differences.iterrows():
                    summary['comparison_data'].append({
                        'scheme': row['Scheme Name'],
                        'regular_reduction': float(row['TER Reduction (%)_Regular']),
                        'direct_reduction': float(row['TER Reduction (%)_Direct']),
                        'difference': float(row['Difference (%)'])
                    })
                logger.info(f"Comparison: {summary['comparison_count']} schemes")
            except Exception as e:
                logger.warning(f"Could not read Comparison file: {e}")
    
    # Write summary to JSON for GitHub Actions
    try:
        with open('analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary: Regular={summary['regular_count']}, Direct={summary['direct_count']}, Comparison={summary['comparison_count']}")
    except Exception as e:
        logger.error(f"Error writing summary: {e}")
    
    return summary

if __name__ == '__main__':
    try:
        analyze_daily()
        generate_notification_data()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        exit(1)
