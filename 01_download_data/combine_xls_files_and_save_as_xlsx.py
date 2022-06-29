import pandas as pd
from pathlib import Path
import argparse

# Requires packages lxml and openpyxl
# Install with conda install lxml, conda install openpyxl

# Example command:
# python combine_xls_files_and_save_as_xlsx.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_xls_20210101_20220617 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\01_download_cc\01.1_xls_20210101_20220617\20210101_20220617_xls_combined.xlsx

# Overall structure:
# Go into a folder.
# Combine all the "xls" files.
# Save into an actual excel file, in .xlsx format.

# Read in command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine .xls files from Thomson One. The key point to note is that the so-called .xls files are actually .html files in disguise.')
    parser.add_argument('inputfolder', help="inputfolder containing the .xls files", type=str)
    parser.add_argument('outputfilepath', help="output file path, e.g. C:\\...\\xlsfiles.xlsx", type=str)
    args = parser.parse_args()

    inputfolder = Path(args.inputfolder)
    outputfilepath = Path(args.outputfilepath)

# Read in ".xls" files (which are really .html files)
table = pd.DataFrame()
for file in inputfolder.iterdir(): 
    if file.suffix == '.xls':
        print("Reading:", file)
        # Read .html file into a pandas df and append to larger table
        chunktable = pd.read_html(file)[0]
        chunktable['filename'] = file.name
        table = pd.concat([table, chunktable])

# Save table into excel
print("\nSaving xls combined into:", outputfilepath)
writer = pd.ExcelWriter(outputfilepath)
table.to_excel(writer, sheet_name='xls_combined')
writer.save()
print("Saved!")


