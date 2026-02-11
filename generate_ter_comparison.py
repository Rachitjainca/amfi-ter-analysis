import pandas as pd
import os
import sys

print("=" * 80)
print("TER Comparison Report Generator")
print("=" * 80)

# List what files we have
print("\n📁 Checking for required files...")
direct_file = './output/Direct_Plan_TER_Changes.csv'
regular_file = './output/Regular_Plan_TER_Changes.csv'

if not os.path.exists(direct_file):
    print(f"❌ Missing: {direct_file}")
else:
    print(f"✅ Found: {direct_file}")

if not os.path.exists(regular_file):
    print(f"❌ Missing: {regular_file}")
else:
    print(f"✅ Found: {regular_file}")

# Read both CSV files with error handling
print("\n📖 Reading CSV files...")
try:
    direct_df = pd.read_csv(direct_file)
    print(f"✅ Loaded Direct Plan data: {len(direct_df)} records")
    regular_df = pd.read_csv(regular_file)
    print(f"✅ Loaded Regular Plan data: {len(regular_df)} records")
except FileNotFoundError as e:
    print(f"\n❌ ERROR: Required CSV files not found")
    print(f"Details: {e}")
    print("\nPlease ensure:")
    print("1. TER analysis workflow has completed successfully")
    print("2. CSV files have been committed to the repository")
    print("3. Latest changes have been pulled")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERROR: Failed to read CSV files")
    print(f"Details: {e}")
    sys.exit(1)

# Rename columns for clarity
direct_df = direct_df.rename(columns={
    'Old Direct Plan - Base TER (%)': 'Direct_Old_TER',
    'New Direct Plan - Base TER (%)': 'Direct_New_TER',
    'TER Date (Change)': 'TER_Date'
})

regular_df = regular_df.rename(columns={
    'Old Regular Plan - Base TER (%)': 'Regular_Old_TER',
    'New Regular Plan - Base TER (%)': 'Regular_New_TER',
    'TER Date (Change)': 'TER_Date'
})

# Select necessary columns
direct_df = direct_df[['NSDL Scheme Code', 'Scheme Name', 'TER_Date', 'Direct_Old_TER', 'Direct_New_TER']]
regular_df = regular_df[['NSDL Scheme Code', 'Scheme Name', 'TER_Date', 'Regular_Old_TER', 'Regular_New_TER']]

# Merge on NSDL Scheme Code and Scheme Name
merged_df = pd.merge(direct_df, regular_df, on=['NSDL Scheme Code', 'Scheme Name'], how='outer')

# Handle TER_Date from both dataframes (they should be the same, but just in case)
merged_df['TER_Date'] = merged_df['TER_Date_x'].fillna(merged_df['TER_Date_y'])
merged_df = merged_df.drop(['TER_Date_x', 'TER_Date_y'], axis=1)

# Calculate changes
merged_df['Regular_Change'] = merged_df['Regular_New_TER'] - merged_df['Regular_Old_TER']
merged_df['Direct_Change'] = merged_df['Direct_New_TER'] - merged_df['Direct_Old_TER']

# Calculate the difference between changes (Regular change - Direct change)
merged_df['Difference_in_Changes'] = merged_df['Regular_Change'] - merged_df['Direct_Change']

# Create final output with required columns
output_df = merged_df[[
    'Scheme Name',
    'TER_Date',
    'Regular_Old_TER',
    'Regular_New_TER',
    'Direct_Old_TER',
    'Direct_New_TER',
    'Difference_in_Changes'
]].copy()

# Rename columns for clarity in output
output_df = output_df.rename(columns={
    'TER_Date': 'Date of TER Change',
    'Regular_Old_TER': 'Regular Base TER Old',
    'Regular_New_TER': 'Regular Base TER New',
    'Direct_Old_TER': 'Direct Base TER Old',
    'Direct_New_TER': 'Direct Base TER New',
    'Difference_in_Changes': 'Difference (Reg Change - Dir Change)'
})

# Filter: Only schemes with actual changes (not zero changes)
print("\n🔍 Filtering schemes with actual TER changes...")
output_df['Has_Change'] = (output_df['Regular Base TER Old'] != output_df['Regular Base TER New']) | \
                           (output_df['Direct Base TER Old'] != output_df['Direct Base TER New'])
filtered_df = output_df[output_df['Has_Change']].drop('Has_Change', axis=1)
print(f"✅ Schemes with changes: {len(filtered_df)} out of {len(output_df)}")

# Sort by Difference in descending order
filtered_df = filtered_df.sort_values('Difference (Reg Change - Dir Change)', ascending=False).reset_index(drop=True)

# Categorize by fund type
print("\n📂 Categorizing by fund type...")
def categorize_fund(scheme_name):
    scheme_lower = scheme_name.lower()
    if 'equity' in scheme_lower or 'growth' in scheme_lower or 'largecap' in scheme_lower or 'midcap' in scheme_lower or 'smallcap' in scheme_lower:
        return 'Equity'
    elif 'debt' in scheme_lower or 'bond' in scheme_lower or 'duration' in scheme_lower or 'liquid' in scheme_lower or 'gilt' in scheme_lower:
        return 'Debt'
    elif 'hybrid' in scheme_lower or 'balanced' in scheme_lower or 'arbitrage' in scheme_lower or 'savings' in scheme_lower:
        return 'Hybrid/Mixed'
    elif 'index' in scheme_lower or 'nifty' in scheme_lower or 'sensex' in scheme_lower or 'etf' in scheme_lower:
        return 'Index/ETF'
    elif 'fof' in scheme_lower or 'fund of funds' in scheme_lower:
        return 'Fund of Funds'
    else:
        return 'Other'

filtered_df['Fund_Category'] = filtered_df['Scheme Name'].apply(categorize_fund)

# Apply threshold filter (> 0.02)
print("⚙️ Applying threshold filter (Difference > 0.02)...")
threshold = 0.02
significant_df = filtered_df[filtered_df['Difference (Reg Change - Dir Change)'].abs() >= threshold].copy()
print(f"✅ Schemes above threshold (>0.02): {len(significant_df)} out of {len(filtered_df)}\n")

# Group by category
print("📊 Category Distribution:")
for category in sorted(significant_df['Fund_Category'].unique()):
    cat_count = len(significant_df[significant_df['Fund_Category'] == category])
    print(f"  {category}: {cat_count} schemes")

# Save all filtered data (no threshold)
filtered_df.to_csv('./output/TER_Comparison_Comprehensive.csv', index=False)
print(f"\n✅ Saved: TER_Comparison_Comprehensive.csv ({len(filtered_df)} schemes)")

# Save significant changes (with threshold)
significant_df_save = significant_df.drop('Fund_Category', axis=1)
significant_df_save.to_csv('./output/TER_Comparison_Significant.csv', index=False)
print(f"✅ Saved: TER_Comparison_Significant.csv ({len(significant_df)} schemes)")

# Prepare data for Google Chat
print("\n💬 Preparing Google Chat message...")

# Display summary
print("\n" + "=" * 150)
print("FILTERED TER COMPARISON - SCHEMES WITH ACTUAL CHANGES")
print("=" * 150)

# Display top 20 by difference
print("\n🔝 TOP 20 SCHEMES (Highest Difference - Filtered by Category)\n")
top_20_sig = significant_df.head(20)[['Scheme Name', 'Date of TER Change', 'Regular Base TER Old', 
                                        'Regular Base TER New', 'Direct Base TER Old', 'Direct Base TER New', 
                                        'Difference (Reg Change - Dir Change)', 'Fund_Category']]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(top_20_sig.to_string(index=False))

# Summary statistics
print("\n" + "=" * 150)
print("SUMMARY STATISTICS")
print("=" * 150)
print(f"\n📊 Total Analysis:")
print(f"  Total schemes analyzed: {len(output_df)}")
print(f"  Schemes with actual changes: {len(filtered_df)}")
print(f"  Schemes above threshold (>0.02): {len(significant_df)}")

print(f"\n📂 By Fund Category (Significant Changes):")
for category in sorted(significant_df['Fund_Category'].unique()):
    cat_df = significant_df[significant_df['Fund_Category'] == category]
    avg_diff = cat_df['Difference (Reg Change - Dir Change)'].mean()
    print(f"  {category}: {len(cat_df)} schemes (avg diff: {avg_diff:.4f})")

print(f"\n📈 Change Distribution (All Changed Schemes):")
print(f"  Regular change > Direct change: {len(filtered_df[filtered_df['Difference (Reg Change - Dir Change)'] > 0])}")
print(f"  Regular change < Direct change: {len(filtered_df[filtered_df['Difference (Reg Change - Dir Change)'] < 0])}")
print(f"  Regular change = Direct change: {len(filtered_df[filtered_df['Difference (Reg Change - Dir Change)'] == 0])}")

print(f"\n📊 Difference Statistics (All Changed Schemes):")
print(f"  Average: {filtered_df['Difference (Reg Change - Dir Change)'].mean():.4f}")
print(f"  Max: {filtered_df['Difference (Reg Change - Dir Change)'].max():.4f}")
print(f"  Min: {filtered_df['Difference (Reg Change - Dir Change)'].min():.4f}")

print("\n" + "=" * 150)
print(f"Output Files:")
print(f"  ✅ TER_Comparison_Comprehensive.csv - All {len(filtered_df)} changed schemes")
print(f"  ✅ TER_Comparison_Significant.csv - {len(significant_df)} schemes above threshold (>0.02)")
print("=" * 150)
