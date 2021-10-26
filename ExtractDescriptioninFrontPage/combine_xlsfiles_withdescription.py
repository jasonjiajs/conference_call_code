import pandas as pd
from pathlib import Path

inputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage")
#C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage\Converted_onmercury
outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage")
outputfile = "xlscombined_withfrontpagedescription_combined.xlsx"

#xlscombined_withfrontpagedescription_convertedonmercury
#xlscombined_withfrontpagedescription_combined
outputpath = Path(outputfolder / outputfile)

table = pd.DataFrame()
columnstouse = ["Report #", "Frontpagedescription", "Date", "Title", "Subtitle"]

for file in inputfolder.iterdir(): 
    if '.xlsx' in file.name:
        print(file)
        if columnstouse == "All":
            chunktable = pd.read_excel(file, header=0)
        else:
            chunktable = pd.read_excel(file, header=0, usecols=columnstouse)
        table = table.append(chunktable)    

# table = table.rename(columns = {'country':'Report'})    
# table = table.sort_values(by=["Report", "Keywords"])
# table['Date'].isna().sum() #counts number of missing dates in Sixun's reorts - 3787 (correct, checked excel manually).
# table = table.dropna(subset=['Date']) # Use this to drop missing dates
writer = pd.ExcelWriter(outputpath)
table.to_excel(writer, 'files_combined', index=False)
writer.save()
writer.close()

