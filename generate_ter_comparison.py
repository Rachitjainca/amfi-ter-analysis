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

# Sort by Difference in descending order
output_df = output_df.sort_values('Difference (Reg Change - Dir Change)', ascending=False).reset_index(drop=True)

# Save to CSV
output_df.to_csv('./output/TER_Comparison_Comprehensive.csv', index=False)

# Display summary
print("=" * 150)
print("COMPREHENSIVE TER CHANGE COMPARISON TABLE")
print("=" * 150)
print(f"\nTotal schemes with TER changes: {len(output_df)}\n")

# Display with better formatting
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(output_df.to_string(index=False))

print("\n" + "=" * 150)
print(f"Output saved to: ./output/TER_Comparison_Comprehensive.csv")
print("=" * 150)

# Print some statistics
print(f"\nStatistics:")
print(f"  Schemes where Regular change > Direct change: {len(output_df[output_df['Difference (Reg Change - Dir Change)'] > 0])}")
print(f"  Schemes where Regular change < Direct change: {len(output_df[output_df['Difference (Reg Change - Dir Change)'] < 0])}")
print(f"  Schemes where changes are equal: {len(output_df[output_df['Difference (Reg Change - Dir Change)'] == 0])}")
print(f"\nAverage Difference: {output_df['Difference (Reg Change - Dir Change)'].mean():.4f}")
print(f"Max Difference: {output_df['Difference (Reg Change - Dir Change)'].max():.4f}")
print(f"Min Difference: {output_df['Difference (Reg Change - Dir Change)'].min():.4f}")
