import pandas as pd
from pathlib import Path
import os, sys, glob

# Requires packages lxml and openpyxl
# Install with conda install lxml, conda install openpyxl

# Example command (local):
# python combine_xls_files_and_save_as_xlsx.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_xls_20210101_20220617 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_xls_20210101_20220617\20210101_20220617_xls_combined.xlsx

# Overall structure:
# Go into a folder.
# Combine all the "xls" files.
# Save into an actual excel file, in .xlsx format.

# Read in command-line arguments
# Combine .xls files from Thomson One into one .xlsx or .csv file. The key point to note is that the so-called .xls files are actually .html files in disguise.
inputfolder = Path(sys.argv[1])
outputfilepath = Path(sys.argv[2])

# Read in ".xls" files (which are really .html files)
table = pd.DataFrame()
for file in inputfolder.iterdir(): 
    if file.suffix == '.xls':
        print("Reading:", file)
        # Read .html file into a pandas df and append to larger table
        chunktable = pd.read_html(file)[0]
        chunktable['filestem'] = file.stem
        table = pd.concat([table, chunktable])

# Save table into excel or csv
print("\nSaving xls combined into:", outputfilepath)
if outputfilepath.suffix == '.xlsx':
    writer = pd.ExcelWriter(outputfilepath)
    table.to_excel(writer, sheet_name='xls_combined')
    writer.save()
elif outputfilepath.suffix == '.csv':
    table.to_csv(outputfilepath)
print("Saved!")


