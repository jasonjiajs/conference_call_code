# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
path = Path(r"Filtered_Ordered_Amended_Correct_No_IR.csv")
df = pd.read_csv(path)
df = df[["Keyword", "Date", "Report", "File", "Title", "Para", "Subtitle"]]
df = df.rename(columns = {'Keyword':'Keywords','Para':'Paragraph'})
df['Type'] = 'Cri1'
df = df.reindex(columns= ["Keywords", "Date", "Report", "File", "Type", "Title", "Paragraph", "Subtitle"])

df.to_excel(r"TotalCircNew_No_IR_sortof.xlsx")
