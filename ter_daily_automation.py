import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Create directories
os.makedirs('downloads', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('history', exist_ok=True)

# State file to track last processed date and files
STATE_FILE = 'ter_state.json'

def load_state():
    """Load the state of last processed date and files"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'last_processed_date': None,
        'last_month': None,
        'last_year': None,
        'previous_day_file': None
    }

def save_state(state):
    """Save the state of processed date and files"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_current_month_year():
    """Get current month and year"""
    today = datetime.now()
    return today.month, today.year

def download_ter_file(month, year):
    """Download TER file for a specific month and year"""
    month_str = f"{month:02d}-{year}"
    url = f"https://www.amfiindia.com/api/populate-te-rdata-revised?MF_ID=All&Month={month_str}&strCat=-1&strType=-1&excel=true"
    
    print(f"Downloading TER file for {month_str}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60, verify=False)
        print(f"Response status: {response.status_code}, Size: {len(response.content)} bytes")
        
        if response.status_code == 200 and len(response.content) > 100:
            file_path = f"downloads/TER_{month_str}.xlsx"
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded: {file_path}")
            return file_path
        else:
            print(f"✗ Failed to download")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def read_ter_file(file_path):
    """Read Excel file and return dataframe"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return None

def find_ter_columns(df):
    """Find the TER columns in the dataframe"""
    regular_col = None
    direct_col = None
    scheme_code_col = None
    scheme_name_col = None
    
    for col in df.columns:
        col_str = str(col).lower()
        if 'nsdl' in col_str and 'code' in col_str:
            scheme_code_col = col
        if 'scheme name' in col_str:
            scheme_name_col = col
        if 'regular' in col_str and 'base' in col_str and 'ter' in col_str:
            regular_col = col
        if 'direct' in col_str and 'base' in col_str and 'ter' in col_str:
            direct_col = col
    
    return scheme_code_col, scheme_name_col, regular_col, direct_col

def get_current_ter_data(current_month=None, current_year=None):
    """Get current month TER data"""
    if current_month is None or current_year is None:
        current_month, current_year = get_current_month_year()
    
    file_path = f"downloads/TER_{current_month:02d}-{current_year}.xlsx"
    
    if not os.path.exists(file_path):
        downloaded = download_ter_file(current_month, current_year)
        if not downloaded:
            return None
        file_path = downloaded
    
    return read_ter_file(file_path)

def compare_ter_daily(current_df, previous_df):
    """Compare TER changes between current and previous day"""
    
    current_code, current_name, current_regular, current_direct = find_ter_columns(current_df)
    previous_code, previous_name, previous_regular, previous_direct = find_ter_columns(previous_df)
    
    # Create working copies
    current_df = current_df.copy()
    previous_df = previous_df.copy()
    
    if current_code:
        current_df[current_code] = current_df[current_code].astype(str).str.strip()
    if previous_code:
        previous_df[previous_code] = previous_df[previous_code].astype(str).str.strip()
    
    regular_changes = []
    direct_changes = []
    
    # Merge on scheme code for Regular Plan
    if current_code and current_regular and previous_regular and current_name:
        print(f"\nComparing Regular Plan TER changes day-to-day...")
        
        merge_cols = [current_code, current_name, current_regular]
        merged = previous_df[[previous_code, previous_name, previous_regular]].merge(
            current_df[merge_cols],
            left_on=previous_code,
            right_on=current_code,
            how='inner',
            suffixes=('_prev', '_current')
        )
        
        merged[previous_regular] = pd.to_numeric(merged[previous_regular], errors='coerce')
        merged[current_regular] = pd.to_numeric(merged[current_regular], errors='coerce')
        
        mask = (merged[previous_regular] != merged[current_regular]) & (merged[previous_regular].notna()) & (merged[current_regular].notna())
        changed = merged[mask]
        
        print(f"Found {len(changed)} changes")
        
        for _, row in changed.iterrows():
            regular_changes.append({
                'NSDL Scheme Code': row[current_code],
                'Scheme Name': row[current_name],
                'Previous Regular Plan - Base TER (%)': round(float(row[previous_regular]), 4),
                'Current Regular Plan - Base TER (%)': round(float(row[current_regular]), 4),
                'TER Date (Change)': datetime.now().strftime('%Y-%m-%d'),
                'TER Reduction (%)': round(float(row[previous_regular] - row[current_regular]), 4)
            })
    
    # Merge on scheme code for Direct Plan
    if current_code and current_direct and previous_direct and current_name:
        print(f"Comparing Direct Plan TER changes day-to-day...")
        
        merge_cols = [current_code, current_name, current_direct]
        merged = previous_df[[previous_code, previous_name, previous_direct]].merge(
            current_df[merge_cols],
            left_on=previous_code,
            right_on=current_code,
            how='inner',
            suffixes=('_prev', '_current')
        )
        
        merged[previous_direct] = pd.to_numeric(merged[previous_direct], errors='coerce')
        merged[current_direct] = pd.to_numeric(merged[current_direct], errors='coerce')
        
        mask = (merged[previous_direct] != merged[current_direct]) & (merged[previous_direct].notna()) & (merged[current_direct].notna())
        changed = merged[mask]
        
        print(f"Found {len(changed)} changes")
        
        for _, row in changed.iterrows():
            direct_changes.append({
                'NSDL Scheme Code': row[current_code],
                'Scheme Name': row[current_name],
                'Previous Direct Plan - Base TER (%)': round(float(row[previous_direct]), 4),
                'Current Direct Plan - Base TER (%)': round(float(row[current_direct]), 4),
                'TER Date (Change)': datetime.now().strftime('%Y-%m-%d'),
                'TER Reduction (%)': round(float(row[previous_direct] - row[current_direct]), 4)
            })
    
    return regular_changes, direct_changes

def save_daily_results(regular_changes, direct_changes, date_str):
    """Save daily results to timestamped files"""
    
    if regular_changes:
        regular_df = pd.DataFrame(regular_changes)
        regular_df = regular_df.sort_values('NSDL Scheme Code').drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        output_file = f'output/Daily_Regular_Plan_Changes_{date_str}.csv'
        regular_df.to_csv(output_file, index=False)
        print(f"\nSaved Regular Plan changes: {output_file}")
    
    if direct_changes:
        direct_df = pd.DataFrame(direct_changes)
        direct_df = direct_df.sort_values('NSDL Scheme Code').drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        output_file = f'output/Daily_Direct_Plan_Changes_{date_str}.csv'
        direct_df.to_csv(output_file, index=False)
        print(f"Saved Direct Plan changes: {output_file}")

def main():
    print("=" * 100)
    print("AMFI TER (Total Expense Ratio) - Daily Automated Analysis")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    # Load state
    state = load_state()
    current_month, current_year = get_current_month_year()
    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')
    
    print(f"\nCurrent Date: {today_str}")
    print(f"Current Month: {current_month:02d}-{current_year}")
    print(f"Last Processed: {state.get('last_processed_date', 'Never')}")
    
    # Check if already processed today
    if state.get('last_processed_date') == today_str:
        print("\n✓ Already processed today. Skipping...")
        return
    
    # Check if month changed, download new month file
    last_month = state.get('last_month')
    last_year = state.get('last_year')
    
    if last_month != current_month or last_year != current_year:
        print(f"\n1. Month changed! Downloading new data...")
        if last_month is not None:
            print(f"   Previous: {last_month:02d}-{last_year} → Current: {current_month:02d}-{current_year}")
        
        current_file = download_ter_file(current_month, current_year)
        if not current_file:
            print("✗ Failed to download current month file")
            return
        
        current_df = read_ter_file(current_file)
        if current_df is None:
            print("✗ Failed to read current month file")
            return
        
        # Save current data to history
        timestamp = today.strftime('%Y%m%d')
        history_file = f'history/TER_Data_{current_month:02d}-{current_year}_{timestamp}.pkl'
        current_df.to_pickle(history_file)
        print(f"✓ Saved current data snapshot: {history_file}")
        
        print("\n✓ Month data downloaded successfully")
        print("Next: Daily analysis will start from tomorrow")
        
        state['last_month'] = current_month
        state['last_year'] = current_year
        state['last_processed_date'] = today_str
        state['previous_day_file'] = history_file
        save_state(state)
        print("✓ State saved")
        return
    
    # Daily comparison
    print(f"\n2. Running daily comparison...")
    
    previous_day_file = state.get('previous_day_file')
    
    if previous_day_file and os.path.exists(previous_day_file):
        print(f"   Loading previous day data...")
        previous_df = pd.read_pickle(previous_day_file)
        
        # Get current day data
        current_file = download_ter_file(current_month, current_year)
        if not current_file:
            print("✗ Failed to download current data")
            return
        
        current_df = read_ter_file(current_file)
        if current_df is None:
            print("✗ Failed to read current data")
            return
        
        # Compare
        print(f"\n3. Comparing changes...")
        regular_changes, direct_changes = compare_ter_daily(current_df, previous_df)
        
        if regular_changes or direct_changes:
            print(f"\n4. Saving results...")
            date_str = today.strftime('%Y-%m-%d')
            save_daily_results(regular_changes, direct_changes, date_str)
            
            print(f"\n{'='*100}")
            print(f"SUMMARY FOR {date_str}")
            print(f"{'='*100}")
            print(f"Regular Plan - Schemes with TER changes: {len(regular_changes)}")
            print(f"Direct Plan - Schemes with TER changes: {len(direct_changes)}")
        else:
            print(f"\n✓ No TER changes detected today")
        
        # Save current data for next day
        timestamp = today.strftime('%Y%m%d')
        history_file = f'history/TER_Data_{current_month:02d}-{current_year}_{timestamp}.pkl'
        current_df.to_pickle(history_file)
        state['previous_day_file'] = history_file
    else:
        print(f"   No previous day data found. Downloading current month data...")
        current_file = download_ter_file(current_month, current_year)
        if current_file:
            current_df = read_ter_file(current_file)
            if current_df:
                timestamp = today.strftime('%Y%m%d')
                history_file = f'history/TER_Data_{current_month:02d}-{current_year}_{timestamp}.pkl'
                current_df.to_pickle(history_file)
                state['previous_day_file'] = history_file
                print(f"✓ Baseline data saved for next day comparison")
    
    state['last_processed_date'] = today_str
    state['last_month'] = current_month
    state['last_year'] = current_year
    save_state(state)
    
    print(f"\n{'='*100}")
    print("✓ Analysis complete!")
    print("=" * 100)

if __name__ == "__main__":
    main()
