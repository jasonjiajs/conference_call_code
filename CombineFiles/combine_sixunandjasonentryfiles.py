import pandas as pd
from pathlib import Path

jason_entryfiles = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Jason's reports - missingdatesnotdropped\entryfiles_combined_jason.xlsx")
sixun_entryfiles = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\From Sixun's Reports\entryfiles_combined_sixun.xlsx")
outputfile = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\entry_files_combined\entryfiles_combined_sixunandjason.xlsx")
# At this stage, both entry files don't have any entries with missing dates.

jasontable = pd.read_excel(jason_entryfiles)
sixuntable = pd.read_excel(sixun_entryfiles) 

table = sixuntable.append(jasontable)

#a = table[70000:70002]
print(table.duplicated().sum())

writer = pd.ExcelWriter(outputfile)
table.to_excel(writer, 'files_combined', index=False)
writer.save()           
writer.close()
