import pandas as pd
from pathlib import Path
import re

inputpath = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage\xlscombined_withfrontpagedescription_combined.xlsx")
ogentryfilepath = Path(r'C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\ConferenceCalls_Combined_v4\entryfiles_combined_v4.xlsx')
outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage")
outputfile = Path(r"entryfiles_combined_withfrontpagedescriptions.xlsx")
outputpath = Path(outputfolder / outputfile)

inputdf = pd.read_excel(inputpath) # You can just load 2 columns in, but I wanted to see the data

# Cleaning the Front Page Descriptions
inputdf = inputdf.drop_duplicates() 
test = inputdf['Frontpagedescription'].str.strip()
test = test.replace(to_replace='^[0-9]{1,3}', value='', regex=True).str.strip()
test = test.replace(to_replace='^[0-9]{1,3}', value='', regex=True).str.strip()
test = test.replace(to_replace='Transcript produced and provided by', value='', regex=True).str.strip()
test = test.replace(to_replace='Fair Disclosure Financial Network, Inc. For more information: www.fdfn.com', value='', regex=True).str.strip()
test = test.replace(to_replace='Event Duration: [0-9]{1,2} minutes', value='', regex=True).str.strip() 
test = test.replace(to_replace='[0-9]{2}/[0-9]{2}/[0-9]{4}', value='', regex=True).str.strip()
test = test.replace(to_replace='[0-9]{2}/[0-9]{2}/[0-9]{4}', value='', regex=True).str.strip()
test = test.replace(to_replace='^[0-9]{1,3}', value='', regex=True).str.strip()
test = test.replace(to_replace='^[0-9]{1,3}', value='', regex=True).str.strip()
test = test.replace(to_replace='[\t\n]', value=' ', regex=True).str.strip()
test = test.replace(to_replace=' +', value=' ', regex=True).str.strip()
inputdf['Frontpagedescription'] = test
inputdf2 = inputdf[['Report #', 'Frontpagedescription']]
duplicated = inputdf2[inputdf2.duplicated('Report #')]
inputdf2 = inputdf2.drop_duplicates('Report #')

ogentryfiledf = pd.read_excel(ogentryfilepath)
 
newentryfiledf = ogentryfiledf.merge(inputdf2, left_on='Report', right_on='Report #', 
                                   how='left', validate='m:1')

# newentryfiledf.rename(columns = {'old_col1':'Frontpagedescription'}, inplace = True)

missingfrontpagedesc = newentryfiledf[newentryfiledf['Frontpagedescription'].isna()]
newentryfiledf['Frontpagedescription'].isna().sum()
 
# newentryfiles['Frontpagedescription'].fillna(newentryfiles['Date_right'], inplace = True)

newentryfiledf = newentryfiledf.drop(columns='Report #')
 
writer = pd.ExcelWriter(outputpath)
newentryfiledf.to_excel(writer, 'Sheet1', index=False)
writer.save()
writer.close()
