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

def compare_ter_changes(jan_df, feb_df):
    """Compare TER changes between January and February at scheme level"""
    
    jan_code, jan_name, jan_regular, jan_direct = find_ter_columns(jan_df)
    feb_code, feb_name, feb_regular, feb_direct = find_ter_columns(feb_df)
    
    print(f"\nJanuary columns - Code: {jan_code}, Name: {jan_name}, Regular: {jan_regular}, Direct: {jan_direct}")
    print(f"February columns - Code: {feb_code}, Name: {feb_name}, Regular: {feb_regular}, Direct: {feb_direct}")
    
    # Create working copies with consistent types
    jan_df = jan_df.copy()
    feb_df = feb_df.copy()
    
    if jan_code:
        jan_df[jan_code] = jan_df[jan_code].astype(str).str.strip()
    if feb_code:
        feb_df[feb_code] = feb_df[feb_code].astype(str).str.strip()
    
    regular_changes = []
    direct_changes = []
    
    # Merge on scheme code for Regular Plan
    if jan_code and jan_regular and feb_regular and jan_name:
        print(f"\nProcessing Regular Plan TER changes...")
        
        # Merge dataframes on scheme code
        merge_cols = [jan_code, jan_name, jan_regular]
        merged = feb_df[[feb_code, feb_name, feb_regular]].merge(
            jan_df[merge_cols],
            left_on=feb_code,
            right_on=jan_code,
            how='inner',
            suffixes=('_feb', '_jan')
        )
        
        # Convert to numeric and find differences
        merged[jan_regular] = pd.to_numeric(merged[jan_regular], errors='coerce')
        merged[feb_regular] = pd.to_numeric(merged[feb_regular], errors='coerce')
        
        # Filter for changes
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
    
    # Merge on scheme code for Direct Plan
    if jan_code and jan_direct and feb_direct and jan_name:
        print(f"Processing Direct Plan TER changes...")
        
        # Merge dataframes on scheme code
        merge_cols = [jan_code, jan_name, jan_direct]
        merged = feb_df[[feb_code, feb_name, feb_direct]].merge(
            jan_df[merge_cols],
            left_on=feb_code,
            right_on=jan_code,
            how='inner',
            suffixes=('_feb', '_jan')
        )
        
        # Convert to numeric and find differences
        merged[jan_direct] = pd.to_numeric(merged[jan_direct], errors='coerce')
        merged[feb_direct] = pd.to_numeric(merged[feb_direct], errors='coerce')
        
        # Filter for changes
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

def save_results(regular_changes, direct_changes):
    """Save results to CSV files"""
    
    if regular_changes:
        # Deduplicate by keeping only one record per scheme code
        regular_df = pd.DataFrame(regular_changes)
        regular_df = regular_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        regular_df = regular_df.sort_values('NSDL Scheme Code')
        output_file = 'output/Regular_Plan_TER_Changes.csv'
        regular_df.to_csv(output_file, index=False)
        print(f"\n{'='*100}")
        print(f"REGULAR PLAN - BASE TER (%) CHANGES ({len(regular_df)} unique schemes)")
        print(f"{'='*100}")
        print(f"Saved to: {output_file}")
        print("\nSample records (first 15):")
        for i, (_, row) in enumerate(regular_df.head(15).iterrows(), 1):
            print(f"  {i:2d}. {row['NSDL Scheme Code']}: {row['Scheme Name']}")
            print(f"      {row['Old Regular Plan - Base TER (%)']:.4f}% → {row['New Regular Plan - Base TER (%)']:.4f}% ({row['Change']:+.4f}%)")
    else:
        print("\nNo Regular Plan TER changes found")
    
    if direct_changes:
        # Deduplicate by keeping only one record per scheme code
        direct_df = pd.DataFrame(direct_changes)
        direct_df = direct_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
        direct_df = direct_df.sort_values('NSDL Scheme Code')
        output_file = 'output/Direct_Plan_TER_Changes.csv'
        direct_df.to_csv(output_file, index=False)
        print(f"\n{'='*100}")
        print(f"DIRECT PLAN - BASE TER (%) CHANGES ({len(direct_df)} unique schemes)")
        print(f"{'='*100}")
        print(f"Saved to: {output_file}")
        print("\nSample records (first 15):")
        for i, (_, row) in enumerate(direct_df.head(15).iterrows(), 1):
            print(f"  {i:2d}. {row['NSDL Scheme Code']}: {row['Scheme Name']}")
            print(f"      {row['Old Direct Plan - Base TER (%)']:.4f}% → {row['New Direct Plan - Base TER (%)']:.4f}% ({row['Change']:+.4f}%)")
    else:
        print("\nNo Direct Plan TER changes found")

def main():
    print("=" * 80)
    print("AMFI TER (Total Expense Ratio) Analysis - January vs February 2026")
    print("=" * 80)
    
    jan_file = 'downloads/TER_01-2026.xlsx'
    feb_file = 'downloads/TER_02-2026.xlsx'
    
    # Check if files need to be downloaded
    if not os.path.exists(jan_file) or not os.path.exists(feb_file):
        print("\n1. Downloading TER files...")
        if not os.path.exists(jan_file):
            jan_file_dl = download_ter_file(1, 2026)
            if not jan_file_dl:
                print("✗ Failed to download January file")
                return
            jan_file = jan_file_dl
        if not os.path.exists(feb_file):
            feb_file_dl = download_ter_file(2, 2026)
            if not feb_file_dl:
                print("✗ Failed to download February file")
                return
            feb_file = feb_file_dl
    else:
        print("\n1. Files already downloaded, skipping download...")
        print(f"   Using: {jan_file}")
        print(f"   Using: {feb_file}")
    
    print("\n2. Reading Excel files...")
    print("January 2026:")
    jan_df = read_ter_file(jan_file)
    print("February 2026:")
    feb_df = read_ter_file(feb_file)
    
    if jan_df is None or feb_df is None:
        print("\n✗ Failed to read Excel files")
        return
    
    print("\n3. Comparing TER changes...")
    regular_changes, direct_changes = compare_ter_changes(jan_df, feb_df)
    
    print("\n4. Saving results...")
    save_results(regular_changes, direct_changes)
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
