import pandas as pd

print("Deduplicating scheme-level TER changes...")

# Read the files
print("\nProcessing Regular Plan...")
regular_df = pd.read_csv('output/Regular_Plan_TER_Changes.csv')
print(f"  Original records: {len(regular_df)}")

# Keep only first record per scheme code
regular_df = regular_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
regular_df = regular_df.sort_values('NSDL Scheme Code').reset_index(drop=True)
print(f"  Unique schemes: {len(regular_df)}")

# Save cleaned file
regular_df.to_csv('output/Regular_Plan_TER_Changes.csv', index=False)
print(f"  Saved to: output/Regular_Plan_TER_Changes.csv")

print("\nProcessing Direct Plan...")
direct_df = pd.read_csv('output/Direct_Plan_TER_Changes.csv')
print(f"  Original records: {len(direct_df)}")

# Keep only first record per scheme code
direct_df = direct_df.drop_duplicates(subset=['NSDL Scheme Code'], keep='first')
direct_df = direct_df.sort_values('NSDL Scheme Code').reset_index(drop=True)
print(f"  Unique schemes: {len(direct_df)}")

# Save cleaned file
direct_df.to_csv('output/Direct_Plan_TER_Changes.csv', index=False)
print(f"  Saved to: output/Direct_Plan_TER_Changes.csv")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nREGULAR PLAN - BASE TER (%) CHANGES ({len(regular_df)} unique schemes)")
print("\nTop 10 records:")
for i, (_, row) in enumerate(regular_df.head(10).iterrows(), 1):
    print(f"  {i:2d}. {row['NSDL Scheme Code']}: {row['Scheme Name']}")
    print(f"      {row['Old Regular Plan - Base TER (%)']:.4f}% → {row['New Regular Plan - Base TER (%)']:.4f}% ({row['Change']:+.4f}%)")

print(f"\nDIRECT PLAN - BASE TER (%) CHANGES ({len(direct_df)} unique schemes)")
print("\nTop 10 records:")
for i, (_, row) in enumerate(direct_df.head(10).iterrows(), 1):
    print(f"  {i:2d}. {row['NSDL Scheme Code']}: {row['Scheme Name']}")
    print(f"      {row['Old Direct Plan - Base TER (%)']:.4f}% → {row['New Direct Plan - Base TER (%)']:.4f}% ({row['Change']:+.4f}%)")

print("\n" + "="*80)
print("✓ Deduplication complete!")
print("="*80)
