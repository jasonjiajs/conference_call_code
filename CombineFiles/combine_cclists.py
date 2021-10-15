import pandas as pd
from pathlib import Path

# Overall structure:
# Go into a folder.
# Combine all the .xlsx entry files.
# Save into an actual excel file, in .xlsx format.

inputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\CC_List_sixun")
outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\CC_List_sixun")

outputfile = "CC_List_2011-2021.csv"
outputpath = Path(outputfolder / outputfile)

table = pd.DataFrame()

for file in inputfolder.iterdir(): 
    if '.csv' in file.name:
        print(file)
        chunktable = pd.read_csv(file, low_memory = False)
        table = table.append(chunktable)    
        
writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'Sheet1', index=False)
writer.save()
writer.close()

