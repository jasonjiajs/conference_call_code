from pathlib import Path
import pandas as pd
import sys
import gc

# Example command: python merge_and_process_compustat.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\compustat_processed\20220705 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\compustat_processed\20220705\ciqcompany_mergedwithgvkeyandcountry.csv

inputfolder = Path(sys.argv[1])
outputfilepath = Path(sys.argv[2])
 
inputfilename_ciqcompany = 'ciqcompany.csv'
inputfilename_wrds_gvkey = 'wrds_gvkey.csv'
inputfilename_ciqcountrygeo = 'ciqcountrygeo.csv'

# Import files
ciqcompany = pd.read_csv(Path(inputfolder / inputfilename_ciqcompany))
wrds_gvkey = pd.read_csv(Path(inputfolder / inputfilename_wrds_gvkey))
ciqcountrygeo = pd.read_csv(Path(inputfolder / inputfilename_ciqcountrygeo))

# Columns
# ciqcompany.columns: ['companyid', 'companyname', 'countryid']
# wrds_gvkey.columns: ['companyid', 'gvkey', 'startdate', 'enddate', 'companyname']
# ciqcountrygeo.columns: ['countryid', 'country', 'isocountry2', 'isocountry3', 'regionid', 'region']

# Filter wrds_gvkey and ciqcountrygeo to keep relevant columns
wrds_gvkey = wrds_gvkey[['companyid', 'gvkey']]
ciqcountrygeo = ciqcountrygeo[['countryid','country']]

# Check: There are duplicates of company IDs for about 500 firms, because some companies have muliple names. We keep all the names.
value_counts = wrds_gvkey['companyid'].value_counts()
print("Number of duplicated companyids in wrds_gvkey:", value_counts[value_counts > 1].count())

# Check: Some companyids have multiple gvkeys. We keep only the first gvkey.
value_counts = wrds_gvkey['gvkey'].value_counts()
print("Number of duplicated gvkeys in wrds_gvkey:", value_counts[value_counts > 1].count())
wrds_gvkey = wrds_gvkey.drop_duplicates('companyid')

# Idea: Merge ciqcompany with gvkey and country
# 1. Merge ciqcompany with gvkey
ciqcompany = ciqcompany.merge(wrds_gvkey, on='companyid', how='left', validate='1:1')
gc.collect() # Delete collectable items to clear memory

# 2. Merge (ciqcompany, gvkey) with country
ciqcompany = ciqcompany.merge(ciqcountrygeo, on='countryid', how='left', validate='m:1')
gc.collect() # Delete collectable items to clear memory

# Save the merged df into csv
ciqcompany.to_csv(outputfilepath, index = False)
print("Saved merged and processed compustat files to:", outputfilepath)