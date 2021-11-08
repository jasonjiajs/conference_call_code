from pathlib import Path
import pandas as pd

# convert a file from csv to pd
inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification")
inputfile = Path(r"Hassanfile_raw_updated2019030.csv")
inputpath = Path(inputfolder / inputfile)
outputfile1 = inputfile.stem + '_viewable.csv'
outputpath1 = Path(inputfolder / outputfile1)
outputfile2 = inputfile.stem + '_truncated.csv'
outputpath2 = Path(inputfolder / outputfile2)

df = pd.read_csv(inputpath, sep="\t")
df.to_csv(outputpath1, index = None)

variablestokeep = ['gvkey','company_name','ticker','hqcountrycode','date','date_earningscall','isin','cusip']
df2 = df[variablestokeep]
df2.to_csv(outputpath2, index = None)
