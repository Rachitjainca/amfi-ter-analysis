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
