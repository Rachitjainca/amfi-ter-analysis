import requests
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Create directories
os.makedirs('downloads', exist_ok=True)
os.makedirs('output', exist_ok=True)

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
        print(f"  Columns: {df.columns.tolist()}")
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

def compare_ter_data(jan_df, feb_df):
    """Compare TER data between two dataframes"""
    jan_code, jan_name, jan_regular, jan_direct = find_ter_columns(jan_df)
    feb_code, feb_name, feb_regular, feb_direct = find_ter_columns(feb_df)
    
    print(f"\nJanuary columns - Code: {jan_code}, Name: {jan_name}, Regular: {jan_regular}, Direct: {jan_direct}")
    print(f"February columns - Code: {feb_code}, Name: {feb_name}, Regular: {feb_regular}, Direct: {feb_direct}")
    
    jan_df = jan_df.copy()
    feb_df = feb_df.copy()
    
    if jan_code:
        jan_df[jan_code] = jan_df[jan_code].astype(str).str.strip()
    if feb_code:
        feb_df[feb_code] = feb_df[feb_code].astype(str).str.strip()
    
    return jan_code, jan_name, jan_regular, jan_direct, feb_code, feb_name, feb_regular, feb_direct, jan_df, feb_df

def analyze_ter_changes(jan_df, feb_df):
    """Analyze TER changes between two dataframes"""
    jan_code, jan_name, jan_regular, jan_direct, feb_code, feb_name, feb_regular, feb_direct, jan_df, feb_df = compare_ter_data(jan_df, feb_df)
    
    regular_changes = []
    direct_changes = []
    
    if jan_code and jan_regular and feb_regular and jan_name:
        print(f"\nProcessing Regular Plan TER changes...")
        merge_cols = [jan_code, jan_name, jan_regular]
        merged = feb_df[[feb_code, feb_name, feb_regular]].merge(
            jan_df[merge_cols],
            left_on=feb_code,
            right_on=jan_code,
            how='inner',
            suffixes=('_feb', '_jan')
        )
        
        merged[jan_regular] = pd.to_numeric(merged[jan_regular], errors='coerce')
        merged[feb_regular] = pd.to_numeric(merged[feb_regular], errors='coerce')
        
        mask = (merged[jan_regular] != merged[feb_regular]) & (merged[jan_regular].notna()) & (merged[feb_regular].notna())
        changed = merged[mask]
        
        print(f"Found {len(changed)} changes")
        
        for _, row in changed.iterrows():
            regular_changes.append({
                'NSDL Scheme Code': row[jan_code],
                'Scheme Name': row[jan_name],
                'Old Regular Plan - Base TER (%)': round(float(row[jan_regular]), 4),
                'New Regular Plan - Base TER (%)': round(float(row[feb_regular]), 4),
                'TER Date (Change)': '2026-02-01',
                'Change': round(float(row[feb_regular] - row[jan_regular]), 4)
            })
    
    if jan_code and jan_direct and feb_direct and jan_name:
        print(f"Processing Direct Plan TER changes...")
        merge_cols = [jan_code, jan_name, jan_direct]
        merged = feb_df[[feb_code, feb_name, feb_direct]].merge(
            jan_df[merge_cols],
            left_on=feb_code,
            right_on=jan_code,
            how='inner',
            suffixes=('_feb', '_jan')
        )
        
        merged[jan_direct] = pd.to_numeric(merged[jan_direct], errors='coerce')
        merged[feb_direct] = pd.to_numeric(merged[feb_direct], errors='coerce')
        
        mask = (merged[jan_direct] != merged[feb_direct]) & (merged[jan_direct].notna()) & (merged[feb_direct].notna())
        changed = merged[mask]
        
        print(f"Found {len(changed)} changes")
        
        for _, row in changed.iterrows():
            direct_changes.append({
                'NSDL Scheme Code': row[jan_code],
                'Scheme Name': row[jan_name],
                'Old Direct Plan - Base TER (%)': round(float(row[jan_direct]), 4),
                'New Direct Plan - Base TER (%)': round(float(row[feb_direct]), 4),
                'TER Date (Change)': '2026-02-01',
                'Change': round(float(row[feb_direct] - row[jan_direct]), 4)
            })
    
    return regular_changes, direct_changes
