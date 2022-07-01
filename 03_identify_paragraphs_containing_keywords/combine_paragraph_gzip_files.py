import pandas as pd
from pathlib import Path
import argparse

# Example command:
# python combine_paragraph_gzip_files.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\03_identify_paragraphs_containing_keywords\03.1_paragraphs_containing_keywords_20210101-20220617 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\03_identify_paragraphs_containing_keywords\03.1_paragraphs_containing_keywords_20210101-20220617\20210101-20220617_paragraphs_containing_keywords_combined.gzip

# Overall structure:
# Go into a folder.
# Combine all the ".gzip" files.
# Save into a .gzip file.

# Read in command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine .xls files from Thomson One. The key point to note is that the so-called .xls files are actually .html files in disguise.')
    parser.add_argument('inputfolder', help="inputfolder containing the .gzip files", type=str)
    parser.add_argument('outputfilepath', help="output file path, e.g. C:\\...\\...paragraphs_containing_keywords_combined.gzip", type=str)
    args = parser.parse_args()

    inputfolder = Path(args.inputfolder)
    outputfilepath = Path(args.outputfilepath)

# Read in ".xls" files (which are really .html files)
table = pd.DataFrame()
count = 0
for file in inputfolder.iterdir(): 
    if file.suffix == '.gzip' and not('combined' in str(file)):
        print("Reading:", file.name)
        # Read .gzip file into a pandas df and append to larger table
        chunktable = pd.read_parquet(file)
        chunktable['filestem'] = file.stem
        table = pd.concat([table, chunktable])
        count = count + 1

# Save table into excel
print("\nSaving", count, ".gzip files combined into:", outputfilepath)
table.to_parquet(outputfilepath, compression = "gzip")
print("Saved!")


