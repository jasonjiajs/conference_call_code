from pathlib import Path
import pandas as pd
import gc

inputfolder = Path(r'C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification\compustat_csv')
outputfolder = inputfolder
outputfile = 'ciqcompany_mergedwithgvkeyandcountry_andnaivetickers.csv'
outputpath = Path(outputfolder / outputfile)

inputfile_ciqcompany = 'ciqcompany.csv'
inputfile_wrds_gvkey = 'wrds_gvkey.csv'
inputfile_ciqcountrygeo = 'ciqcountrygeo.csv'
inputfile_wrds_ticker = 'wrds_ticker.csv'

""" Base file: company information """
df_ciqcompany = pd.read_csv(Path(inputfolder / inputfile_ciqcompany))
# df_ciqcompany.columns
# Index(['companyid', 'companyname', 'countryid'], dtype='object')

""" Merge with gvkey information"""
df_wrds_gvkey = pd.read_csv(Path(inputfolder / inputfile_wrds_gvkey))
# df_wrds_gvkey.columns
# Index(['companyid', 'gvkey', 'startdate', 'enddate', 'companyname'], dtype='object')
df_wrds_gvkey = df_wrds_gvkey[['companyid', 'gvkey']]

# Note: There are duplicates of company IDs for about 500 firms, because some firms are linked to multiple gvkeys. 
# We capture them all.
df_wrds_gvkey_duplicated = df_wrds_gvkey.duplicated('companyid').sum()

df_ciqcompany = df_ciqcompany.merge(df_wrds_gvkey, on='companyid', how='left', validate='1:m')
del df_wrds_gvkey
gc.collect()

""" Merge with country information """
df_ciqcountrygeo = pd.read_csv(Path(inputfolder / inputfile_ciqcountrygeo))
# df_ciqcountrygeo.columns
# Index(['countryid', 'country', 'isocountry2', 'isocountry3', 'regionid', 'region'], dtype='object')
df_ciqcountrygeo = df_ciqcountrygeo[['countryid','country','isocountry2']]

df_ciqcompany = df_ciqcompany.merge(df_ciqcountrygeo, on='countryid', how='left', validate='m:1')
del df_ciqcountrygeo
gc.collect()


""" Naive method: Merge with ticker information """
df_wrds_ticker = pd.read_csv(Path(inputfolder / inputfile_wrds_ticker))
# Note: There are duplicates of company IDs for close to 4 million tickers, because many firms are linked to multiple tickers.
# We don't merge them but keep them as they are.
df_wrds_ticker_duplicated = df_wrds_ticker.duplicated('companyid').sum()

df_wrds_ticker = df_wrds_ticker.drop_duplicates(keep='last')
df_wrds_ticker = df_wrds_ticker.drop_duplicates(subset='companyid', keep='last')

df_ciqcompany = df_ciqcompany.merge(df_wrds_ticker, on='companyid', how='left', validate='m:1')

del df_wrds_ticker
gc.collect()

""" Save the merged df into csv """
df_ciqcompany.to_csv(outputpath, index = None)
del df_ciqcompany
gc.collect()
