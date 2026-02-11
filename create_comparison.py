import pandas as pd

print("Creating comparison file for Direct vs Regular Plan TER changes...")

# Read both files
print("\nReading Regular Plan file...")
reg_df = pd.read_csv('output/Regular_Plan_TER_Changes.csv')
print(f"Regular Plan: {len(reg_df)} schemes")

print("Reading Direct Plan file...")
dir_df = pd.read_csv('output/Direct_Plan_TER_Changes.csv')
print(f"Direct Plan: {len(dir_df)} schemes")

# Find common schemes (appear in both files)
reg_codes = set(reg_df['NSDL Scheme Code'])
dir_codes = set(dir_df['NSDL Scheme Code'])
common_codes = reg_codes.intersection(dir_codes)

print(f"\nCommon schemes in both files: {len(common_codes)}")

# Create comparison dataframe
comparison_data = []

for code in common_codes:
    reg_row = reg_df[reg_df['NSDL Scheme Code'] == code].iloc[0]
    dir_row = dir_df[dir_df['NSDL Scheme Code'] == code].iloc[0]
    
    # Calculate difference in TER Reduction (Direct vs Regular)
    reduction_diff = dir_row['TER Reduction (%)'] - reg_row['TER Reduction (%)']
    
    comparison_data.append({
        'NSDL Scheme Code': code,
        'Scheme Name': reg_row['Scheme Name'],
        'TER Date (Change)': '2026-02-01',
        'Old Regular Plan - Base TER (%)': reg_row['Old Regular Plan - Base TER (%)'],
        'New Regular Plan - Base TER (%)': reg_row['New Regular Plan - Base TER (%)'],
        'Regular Plan - TER Reduction (%)': reg_row['TER Reduction (%)'],
        'Old Direct Plan - Base TER (%)': dir_row['Old Direct Plan - Base TER (%)'],
        'New Direct Plan - Base TER (%)': dir_row['New Direct Plan - Base TER (%)'],
        'Direct Plan - TER Reduction (%)': dir_row['TER Reduction (%)'],
        'Difference (Direct - Regular) TER Reduction (%)': reduction_diff
    })

comparison_df = pd.DataFrame(comparison_data)
comparison_df = comparison_df.sort_values('NSDL Scheme Code').reset_index(drop=True)

# Save to CSV
output_file = 'output/Direct_vs_Regular_TER_Comparison.csv'
comparison_df.to_csv(output_file, index=False)

print(f"\n{'='*100}")
print(f"DIRECT PLAN VS REGULAR PLAN - BASE TER COMPARISON ({len(comparison_df)} schemes)")
print(f"{'='*100}")
print(f"Saved to: {output_file}")

print("\nTop 15 records:\n")
for i, (_, row) in enumerate(comparison_df.head(15).iterrows(), 1):
    print(f"{i:2d}. {row['NSDL Scheme Code']}: {row['Scheme Name']}")
    print(f"    Regular Plan: {row['Old Regular Plan - Base TER (%)']:.4f}% → {row['New Regular Plan - Base TER (%)']:.4f}% (Reduction: {row['Regular Plan - TER Reduction (%)']:+.4f}%)")
    print(f"    Direct Plan:  {row['Old Direct Plan - Base TER (%)']:.4f}% → {row['New Direct Plan - Base TER (%)']:.4f}% (Reduction: {row['Direct Plan - TER Reduction (%)']:+.4f}%)")
    print(f"    Difference (Direct - Regular): {row['Difference (Direct - Regular) TER Reduction (%)']:+.4f}%\n")

print(f"{'='*100}")
print("✓ Comparison file created successfully!")
print(f"{'='*100}")

# Show summary statistics
print(f"\nSUMMARY STATISTICS:")
print(f"  Schemes with greater Direct Plan reduction: {len(comparison_df[comparison_df['Difference (Direct - Regular) TER Reduction (%)'] > 0])}")
print(f"  Schemes with greater Regular Plan reduction: {len(comparison_df[comparison_df['Difference (Direct - Regular) TER Reduction (%)'] < 0])}")
print(f"  Schemes with equal reductions: {len(comparison_df[comparison_df['Difference (Direct - Regular) TER Reduction (%)'] == 0])}")
