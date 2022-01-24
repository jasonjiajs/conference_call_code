import pandas as pd
from pathlib import Path
import argparse

# Overall structure:
# Go into a folder.
# Combine all the "xls" files.
# Save into an actual excel file, in .xlsx format.

# Read in command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine .xls files from Thomson One. The key point to note is that the so-called .xls files are actually .html files in disguise.')
    parser.add_argument('inputfolder', help="inputfolder containing the .xls files. will also be the output folder", type=str)
    parser.add_argument('outputfile', help="output file name, e.g. xlsfiles.xlsx", type=str)
    args = parser.parse_args()

    inputfolder = Path(args.inputfolder)
    outputfolder = inputfolder
    outputfile = args.outputfile
    outputpath = Path(outputfolder / outputfile)


# Previous input / output folders
# "C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles"
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing\Filezilla
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Titles Still Missing in v3
# C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles

# Previous output files:
# "xlshtmlfiles_combined.xlsx"

table = pd.DataFrame()

for file in inputfolder.iterdir(): 
    if 'xls' in file.name:
        print(file)
        chunktable = pd.read_html(file)[0]
        # chunktable = chunktable[['Date','Report #']]
        table = table.append(chunktable)    

writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'files_combined')
writer.save()


