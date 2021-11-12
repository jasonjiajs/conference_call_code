from pathlib import Path
import pandas as pd

# convert a file from csv to pd
inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification\Hassan")
inputfile = Path(r"Hassanfile_raw_updated2019030.csv")
inputpath = Path(inputfolder / inputfile)
#outputfile1 = inputfile.stem + '_viewable.csv'
#outputpath1 = Path(inputfolder / outputfile1)
outputfile2 = inputfile.stem + '_truncated1.csv'
outputpath2 = Path(inputfolder / outputfile2)
outputfile3 = inputfile.stem + '_truncated2.csv'
outputpath3 = Path(inputfolder / outputfile3)
outputfile4 = inputfile.stem + '_truncated3.csv'
outputpath4 = Path(inputfolder / outputfile4)

df = pd.read_csv(inputpath, sep="\t")
#df.to_csv(outputpath1, index = None)

variablestokeep = ['gvkey','company_name','ticker','hqcountrycode','date']
df2 = df[variablestokeep]
df2.to_csv(outputpath2, index = None)

df3 = df2.drop_duplicates(subset=['company_name'], keep='first')
df3.to_csv(outputpath3, index = None)

variablestokeep2 = ['gvkey','company_name','ticker']
df4 = df3[variablestokeep2]
df4.to_csv(outputpath4, index = None)