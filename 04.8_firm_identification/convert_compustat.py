from sas7bdat import SAS7BDAT
from pathlib import Path
import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Compustat .sas7bdat files to .csv files.')
    parser.add_argument('inputfolder', help="input folder containing the .sas7bdat files.", type=str)
    parser.add_argument('outputfolder', help="output folder that will contain the .csv files", type=str)
    args = parser.parse_args()
    inputfolder = Path(args.inputfolder)
    outputfolder = Path(args.outputfolder)

for file in inputfolder.iterdir():
    filestem = file.stem
    if file.suffix == '.sas7bdat':
        outputfile = filestem + '.csv'
        outputpath = Path(outputfolder / outputfile)
        if outputpath.exists() == False:
            inputpath = Path(inputfolder / file)
            with SAS7BDAT(str(inputpath)) as reader:
                df = reader.to_data_frame()
            df.to_csv(outputpath, index = None)
            print("Converted from .sas7bdat to .csv: {}".format(file.name))
        else:
            print(".csv file already exists, did not convert: {}".format(file.name))
