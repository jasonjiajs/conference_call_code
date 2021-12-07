from pathlib import Path
import pandas as pd
import argparse

# convert a file from csv to pd
# previously ended with '_truncated3.csv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Hassan .csv file viewable on Excel, and truncate it by removing unnecessary columns.')
    parser.add_argument('inputfolder', help="input folder containing the .Hassan file.", type=str)
    parser.add_argument('inputfile', help="input file name / Name of the Hassan file, e.g. Hassanfile_raw_updated2019030.csv", type=str)
    parser.add_argument('outputfolder', help="output folder that will contain the .csv files", type=str)
    args = parser.parse_args()
    inputfolder = Path(args.inputfolder)
    inputfile = Path(args.inputfile)
    outputfolder = Path(args.outputfolder)
    inputpath = Path(inputfolder / inputfile)
    outputfile = inputfile.stem + '_processed.csv'
    outputpath = Path(outputfolder / outputfile)

df = pd.read_csv(inputpath, sep="\t")

variablestokeep = ['gvkey','company_name','ticker']
df2 = df[variablestokeep]

df2 = df2.drop_duplicates(subset=['company_name'], keep='first')

df2.to_csv(outputpath, index = None)