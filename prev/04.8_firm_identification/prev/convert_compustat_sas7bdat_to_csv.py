from sas7bdat import SAS7BDAT
from pathlib import Path
import pandas as pd
import argparse

# Example command: python convert_compustat_sas7bdat_to_csv.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\compustat_raw\20220705 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\04_match_firm_names_to_gvkeys\04.1_process_compustat_and_hassan_files\compustat_processed\20220705

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Compustat .sas7bdat files to .csv files.')
    parser.add_argument('inputfolder', help="input folder containing the .sas7bdat files.", type=str)
    parser.add_argument('outputfolder', help="output folder that will contain the .csv files", type=str)
    args = parser.parse_args()
    inputfolder = Path(args.inputfolder)
    outputfolder = Path(args.outputfolder)

for file in inputfolder.iterdir():
    if file.suffix == '.sas7bdat':
        outputfile = file.stem + '.csv'
        outputfilepath = Path(outputfolder / outputfile)
        if outputfilepath.exists() == False:
            inputfilepath = Path(inputfolder / file)
            with SAS7BDAT(str(inputfilepath)) as reader:
                df = reader.to_data_frame()
            df.to_csv(outputfilepath, index = False)
            print("Converted from .sas7bdat to .csv: {}".format(file.name))
        else:
            print(".csv file already exists, did not convert: {}".format(file.name))
