import pandas as pd
from pathlib import Path
import numpy as np

inputpath = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\sixunandjason\v5\missingtitles\reportidswithmissingtitles_betweenv5combinedandthenewone.xlsx")
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\ExtractDescriptioninFrontPage\missingfrontpagedescriptions.xlsx
df = pd.read_excel(inputpath, header=None)

maxnumberofsearches = 25
q, _ = divmod(np.arange(len(df)), maxnumberofsearches)
groups = list(df.groupby(q))
searchterms = []
numberofsearchterms = max(q) + 1
 
for i in range(numberofsearchterms):
    chunk = groups[i][1]
    chunk = chunk.to_csv(header=False, index=False).strip('\n').split('\n')
    chunk = '; '.join(chunk).replace('\r','').replace('\n','')
    searchterms += [chunk]
    print(chunk)
    print("\n")
    
