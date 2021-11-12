# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
path = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\TotalCircnew\Small_No_IR.csv")
df = pd.read_csv(path)
df = df[["Keyword", "Date", "Report", "File", "Title", "Para", "Subtitle"]]
df = df.rename(columns = {'Keyword':'Keywords','Para':'Paragraph'})
df['Type'] = 'Cri1'
df = df.reindex(columns= ["Keywords", "Date", "Report", "File", "Type", "Title", "Paragraph", "Subtitle"])

df.to_excel(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\KeywordIdentification\TotalCircnew\TotalCircNew_Small_No_IR_sortof.xlsx")