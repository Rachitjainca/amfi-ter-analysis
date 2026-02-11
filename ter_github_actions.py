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
    
    # Save today's TER data as baseline for next day comparison
    try:
        baseline_file = 'baseline_ter_data.csv'
        # Save current TER data to use as baseline for tomorrow
        current_df.to_csv(baseline_file, index=False)
        logger.info(f"Baseline TER data saved to {baseline_file}")
    except Exception as e:
        logger.error(f"Error saving baseline data: {e}")
    
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
                comparison['Abs Difference (%)'] = comparison['Difference (%)'].abs()
                # Sort by absolute difference descending
                comparison = comparison.sort_values('Abs Difference (%)', ascending=False)
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

def generate_notification():
    """Generate notification message and summary data in a single pass"""
    output_dir = Path('output')
    summary = {
        'date': str(datetime.now().date()),
        'regular_count': 0,
        'direct_count': 0,
        'comparison_count': 0
    }
    
    # Read data files
    regular_data = None
    direct_data = None
    previous_schemes = set()
    
    regular_file = list(output_dir.glob('Regular_Plan_TER_Changes_*.csv')) if output_dir.exists() else []
    if regular_file:
        try:
            regular_data = pd.read_csv(regular_file[0])
            summary['regular_count'] = len(regular_data)
        except Exception as e:
            logger.warning(f"Could not read Regular Plan file: {e}")
    
    direct_file = list(output_dir.glob('Direct_Plan_TER_Changes_*.csv')) if output_dir.exists() else []
    if direct_file:
        try:
            direct_data = pd.read_csv(direct_file[0])
            summary['direct_count'] = len(direct_data)
        except Exception as e:
            logger.warning(f"Could not read Direct Plan file: {e}")
    
    # Load previous baseline to identify NEW changes
    try:
        if Path('baseline_ter_data.csv').exists():
            previous_baseline = pd.read_csv('baseline_ter_data.csv')
            previous_schemes = set(previous_baseline['Scheme Name'].unique())
            logger.info(f"Loaded previous baseline with {len(previous_schemes)} schemes")
    except Exception as e:
        logger.warning(f"Could not load previous baseline: {e}")
    
    # Build message
    message = ""
    if regular_data is not None or direct_data is not None:
        message = "=" * 150 + "\n"
        message += "AMFI MUTUAL FUND - TER REDUCTIONS (REGULAR vs DIRECT PLAN) - SORTED BY HIGHEST DIFFERENCE\n"
        message += "=" * 150 + "\n\n"
        
        # Build combined table efficiently
        regular_schemes = set(regular_data['Scheme Name'].unique()) if regular_data is not None else set()
        direct_schemes = set(direct_data['Scheme Name'].unique()) if direct_data is not None else set()
        all_schemes = sorted(regular_schemes.union(direct_schemes))
        
        combined_rows = []
        new_count = 0
        
        for scheme in all_schemes:
            row = {'Scheme Name': scheme}
            reg_reduction = 0.0
            dir_reduction = 0.0
            
            # Get Regular plan data
            if regular_data is not None:
                reg_data = regular_data[regular_data['Scheme Name'] == scheme]
                if not reg_data.empty:
                    reg_reduction = float(reg_data['TER Reduction (%)'].iloc[0])
                    row['Reg Old TER %'] = f"{float(reg_data['Old Regular Plan - Base TER (%)'].iloc[0]):.2f}"
                    row['Reg New TER %'] = f"{float(reg_data['New Regular Plan - Base TER (%)'].iloc[0]):.2f}"
                    row['Reg Reduction %'] = f"{reg_reduction:.2f}"
                else:
                    row['Reg Old TER %'] = row['Reg New TER %'] = row['Reg Reduction %'] = 'N/A'
            else:
                row['Reg Old TER %'] = row['Reg New TER %'] = row['Reg Reduction %'] = 'N/A'
            
            # Get Direct plan data
            if direct_data is not None:
                dir_data = direct_data[direct_data['Scheme Name'] == scheme]
                if not dir_data.empty:
                    dir_reduction = float(dir_data['TER Reduction (%)'].iloc[0])
                    row['Dir Old TER %'] = f"{float(dir_data['Old Direct Plan - Base TER (%)'].iloc[0]):.2f}"
                    row['Dir New TER %'] = f"{float(dir_data['New Direct Plan - Base TER (%)'].iloc[0]):.2f}"
                    row['Dir Reduction %'] = f"{dir_reduction:.2f}"
                else:
                    row['Dir Old TER %'] = row['Dir New TER %'] = row['Dir Reduction %'] = 'N/A'
            else:
                row['Dir Old TER %'] = row['Dir New TER %'] = row['Dir Reduction %'] = 'N/A'
            
            row['Difference %'] = reg_reduction - dir_reduction if (reg_reduction and dir_reduction) else 0
            if scheme not in previous_schemes:
                new_count += 1
            
            combined_rows.append(row)
        
        # Convert to DataFrame and sort
        combined_df = pd.DataFrame(combined_rows)
        combined_df['Diff_Value'] = combined_df['Difference %'].astype(float)
        combined_df = combined_df.sort_values('Diff_Value', ascending=False, key=abs)
        
        # Create table output
        display_cols = ['Scheme Name', 'Reg Old TER %', 'Reg New TER %', 'Reg Reduction %', 
                       'Dir Old TER %', 'Dir New TER %', 'Dir Reduction %', 'Difference %']
        message += combined_df[display_cols].to_string(index=False)
        message += "\n\n"
        
        # Add summary
        message += "=" * 150 + "\n"
        message += "SUMMARY\n"
        message += "=" * 150 + "\n"
        if regular_data is not None:
            message += f"Regular Plan: {len(regular_data)} schemes with TER reductions\n"
        if direct_data is not None:
            message += f"Direct Plan: {len(direct_data)} schemes with TER reductions\n"
        message += f"NEW Changes (since last update): {new_count} schemes\n\n"
    else:
        message = "No TER change data available for today."
    
    # Save message
    try:
        with open('notification_message.txt', 'w', encoding='utf-8') as f:
            f.write(message)
        logger.info("Notification message saved")
    except Exception as e:
        logger.error(f"Error saving notification message: {e}")
    
    # Write summary JSON
    try:
        with open('analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary: Regular={summary['regular_count']}, Direct={summary['direct_count']}")
    except Exception as e:
        logger.error(f"Error writing summary: {e}")
    
    return message

if __name__ == '__main__':
    try:
        analyze_daily()
        generate_notification()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        exit(1)
