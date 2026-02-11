import pandas as pd
import os

# Read both CSV files
direct_df = pd.read_csv('./output/Direct_Plan_TER_Changes.csv')
regular_df = pd.read_csv('./output/Regular_Plan_TER_Changes.csv')

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
