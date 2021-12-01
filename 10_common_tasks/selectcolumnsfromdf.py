import pandas as pd
from pathlib import Path

inputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Both Sixun and Jason's reports")
inputfile = Path(r"entryfiles_combined_sixunandjason_missingdatesnotdropped.xlsx")
inputfilepath = Path(inputfolder / inputfile)

outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Both Sixun and Jason's reports")
outputfile = Path(r"entryfiles_combined_sixunandjason_missingdatesnotdropped_droppedsomecols.xlsx")
outputfilepath = Path(outputfolder/outputfile)

df = pd.read_excel(inputfilepath)
print(df.columns)

colstouse = ["Report", "Keywords", "Date", "Title", "Subtitle"]
df = df[colstouse]

writer = pd.ExcelWriter(outputfilepath)
df.to_excel(writer, 'Sheet1', index=False)
writer.save()           
writer.close()