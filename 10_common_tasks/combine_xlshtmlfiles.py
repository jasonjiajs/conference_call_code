import pandas as pd
from pathlib import Path

# Overall structure:
# Go into a folder.
# Combine all the "xls" files.
# Save into an actual excel file, in .xlsx format.

inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles")
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing\Filezilla
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Titles Still Missing in v3
# C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles
outputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles")
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Dates and Titles Missing\Filezilla
# C:\Users\jasonjia\Dropbox\ConferenceCall\Misc\Why are Titles Still Missing in v3
# C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\Not Part of Processing Pipeline\Checkreportidstallywithtitles
outputfile = "xlshtmlfiles_combined.xlsx"
outputpath = Path(outputfolder / outputfile)

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


