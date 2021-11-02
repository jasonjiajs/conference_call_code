from sas7bdat import SAS7BDAT
from pathlib import Path
import pandas as pd

inputfolder = Path(r'C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification')
outputfolder = inputfolder
outputsuffix = ''

for file in inputfolder.iterdir():
    filestem = file.stem
    if file.suffix == '.sas7bdat':
        outputfile = filestem + outputsuffix + '.csv'
        outputpath = Path(outputfolder / outputfile)
        if outputpath.exists() == False:
            inputpath = Path(inputfolder / file)
            with SAS7BDAT(str(inputpath)) as reader:
                df = reader.to_data_frame()
            df.to_csv(outputpath, index = None)
            print("Converted from .sas7bdat to .csv: {}".format(filestem + file.suffix))
