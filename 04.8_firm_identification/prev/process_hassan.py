from pathlib import Path
import pandas as pd
import argparse

# Example command: python process_hassan.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\hassan_raw\20220331\hassan_raw.txt C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\hassan_processed\20220331\hassan_processed.csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Hassan .csv file viewable on Excel, and truncate it by removing unnecessary columns.')
    parser.add_argument('inputfilepath', help="inputfilepath of the raw Hassan file.", type=str)
    parser.add_argument('outputfilepath', help="outputfilepath that contains processed and truncated hassan file", type=str)
    args = parser.parse_args()
    inputfilepath = Path(args.inputfilepath)
    outputfilepath = Path(args.outputfilepath)

# Import raw Hassan file
df = pd.read_csv(inputfilepath, sep="\t")

# Filter relevant columns
variablestokeep = ['gvkey','company_name']
df = df[variablestokeep]

# Drop rows with duplicate company names
df = df.drop_duplicates(subset=['company_name'], keep='first')

# Save df to csv
df.to_csv(outputfilepath, index = None)
print("Saved processed and truncated Hassan file to:", outputfilepath)