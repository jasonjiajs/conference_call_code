import pandas as pd
from pathlib import Path

# Overall structure:
# Go into a folder.
# Combine all the .xlsx entry files.
# Save into an actual excel file, in .xlsx format.

#inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\ConferenceCalls_2020-2021_v2")
#outputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\jason")

#inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files\Sixun\v0 - originalfrommercury")
#outputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\sixun")
#outputfile = "entryfiles_combined_jason_v2withparagraphs.xlsx"
#outputfile = "entryfiles_combined_sixun_v0_withparagraphs.xlsx"

outputpath = Path(outputfolder / outputfile)

table = pd.DataFrame()
columnstouse = ["Report", "Keywords", "Date", "Title", "Subtitle", "Paragraph", "gvkey"]

for file in inputfolder.iterdir(): 
    if '.xlsx' in file.name:
        print(file)
        if columnstouse == "All":
            chunktable = pd.read_excel(file, header=1)
        else:
            chunktable = pd.read_excel(file, header=1, usecols=columnstouse)
        table = table.append(chunktable)    

table = table.sort_values(by=["Report", "Keywords"])
# table['Date'].isna().sum() #counts number of missing dates in Sixun's reorts - 3787 (correct, checked excel manually).
# table = table.dropna(subset=['Date']) # Use this to drop missing dates
writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'files_combined', index=False)
writer.save()
writer.close()

