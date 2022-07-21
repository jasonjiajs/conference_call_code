import pandas as pd
from pathlib import Path
import argparse

# Overall structure:
# Go into a folder.
# Combine all the .xlsx entry files.
# Save into an actual excel file, in .xlsx format.

# Read in command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine entry files.')
    parser.add_argument('inputfolder', help="inputfolder containing the .xls files", type=str)
    parser.add_argument('outputfolder', help="outputfolder containing the .xlsx file", type=str)
    parser.add_argument('outputfile', help="output file name, e.g. entryfilescombined.xlsx", type=str)
    args = parser.parse_args()

    inputfolder = Path(args.inputfolder)
    outputfolder = Path(args.outputfolder)
    outputfile = args.outputfile
    outputpath = Path(outputfolder / outputfile)

# inputfolder
#"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files\Sixun\v2 - titlesubtitleadded"
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing\Filezilla
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files\From Jason's Reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files\From Sixun's Reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files

# outputfolder
# "C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\sixun"
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Jason's reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Sixun's reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined
# outputfile = "entryfiles_combined_sixun_v3withparagraphs.xlsx"
# outputpath = Path(outputfolder / outputfile)

table = pd.DataFrame()
# columnstouse = ["Report", "Keywords", "Date", "Title", "Subtitle"]
columnstouse = ["country", "Keywords", "Date", "Title", "Subtitle", "Paragraph", "gvkey"]

for file in inputfolder.iterdir(): 
    if '.xlsx' in file.name:
        print(file)
        if columnstouse == "All":
            chunktable = pd.read_excel(file, header=1)
        else:
            chunktable = pd.read_excel(file, header=1, usecols=columnstouse)
        table = table.append(chunktable)    

table = table.rename(columns = {'country':'Report'})    
table = table.sort_values(by=["Report", "Keywords"])
# table['Date'].isna().sum() #counts number of missing dates in Sixun's reorts - 3787 (correct, checked excel manually).
# table = table.dropna(subset=['Date']) # Use this to drop missing dates
writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'files_combined', index=False)
writer.save()
writer.close()

