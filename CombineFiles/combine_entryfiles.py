import pandas as pd
from pathlib import Path

# Overall structure:
# Go into a folder.
# Combine all the .xlsx entry files.
# Save into an actual excel file, in .xlsx format.

inputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files\From Sixun's Reports")
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing\Filezilla
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files\From Jason's Reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files\From Sixun's Reports
outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Sixun's reports")
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Jason's reports
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Sixun's reports
outputfile = "entryfiles_combined.xlsx"
outputpath = Path(outputfolder / outputfile)

table = pd.DataFrame()
# columnstouse = ['Keywords', 'Date', 'gvkey', 'Title', 'Report']

for file in inputfolder.iterdir(): 
    if '.xlsx' in file.name:
        print(file)
        # chunktable = pd.read_excel(file, header=1, usecols=columnstouse)
        chunktable = pd.read_excel(file, header=1)
        table = table.append(chunktable)    
        
table = table.sort_values(by=['Observation ID'])
# table['Date'].isna().sum() #counts number of missing dates in Sixun's reorts - 3787 (correct, checked excel manually).
table = table.dropna(subset=['Date'])
writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'files_combined', index=False)
writer.save()
writer.close()

