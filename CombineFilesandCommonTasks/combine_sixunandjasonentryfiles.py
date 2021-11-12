import pandas as pd
from pathlib import Path

jason_entryfiles = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\jason\entryfiles_combined_jason_v2withparagraphs.xlsx")
sixun_entryfiles = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\sixun\entryfiles_combined_sixun_v3withparagraphs.xlsx")
outputfile = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\entry_files_combined\entryfiles_combined_sixunandjason_v2-3withparagraphs2.xlsx")
# At this stage, both entry files don't have any entries with missing dates.

jasontable = pd.read_excel(jason_entryfiles)
sixuntable = pd.read_excel(sixun_entryfiles) 

table = sixuntable.append(jasontable)

#a = table[70000:70002]
print(table.duplicated(subset=['Report','Keywords']).sum())
print(table.value_counts)
table.drop_duplicates(subset=['Report','Keywords'], keep='first', inplace=True)
print(table.duplicated(subset=['Report','Keywords']).sum())

writer = pd.ExcelWriter(outputfile)
table.to_excel(writer, 'files_combined', index=False)
writer.save()           
writer.close()
