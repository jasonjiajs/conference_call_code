from pathlib import Path
import pandas as pd
import sys

# Example command: python combine_processed_hassan_and_compustat_files.py 


hassan_filepath = Path(sys.argv[1])
compustat_filepath = Path(sys.argv[2])
outputfilepath = Path(sys.argv[3])

# Import df
hassan = pd.read_csv(hassan_filepath)
compustat = pd.read_csv(compustat_filepath)

# Combine dfs
combined_df = pd.concat([hassan, compustat])

print("Size of processed Hassan df:", hassan.shape)
print("Size of processed Compustat df:", compustat.shape)
print("Size of combined df:", combined_df.shape)

# Remove rows with duplicate firm names
print("Counting rows of df_combined:")
print("Number of rows:", combined_df.shape[0])
print("Number of unique company names:", combined_df['company_name'].nunique())
combined_df = combined_df.drop_duplicates('company_name')

print("Remove rows with duplicate firm names, recounting rows:")
print("Number of rows:", combined_df.shape[0])
print("Number of unique company names:", combined_df['company_name'].nunique())

# Clean firm names with the same function used to clean firm names for conference calls, in entryfilescombined.

# Remove rows with duplicate firm names

# Save as .csv
print("This combined df forms the set of Compustat and Hassan firm names with gvkeys.")
print("This file will be used to match against firm names for conference calls, in entryfilescombined.")
combined_df.to_csv(outputfilepath, index=False)
print("comvined df saved to:", outputfilepath)