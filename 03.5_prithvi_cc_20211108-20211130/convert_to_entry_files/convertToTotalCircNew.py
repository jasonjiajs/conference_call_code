# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
folder = Path(r"/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1")
path = Path(folder / r"Filtered_Ordered_Amended_Correct_No_IR.csv")
df = pd.read_csv(path)
df = df[["Keyword", "Date", "Report", "File", "Title", "Para", "Subtitle"]]
df = df.rename(columns = {'Keyword':'Keywords','Para':'Paragraph'})
df['Type'] = 'Cri1'
df = df.reindex(columns= ["Keywords", "Date", "Report", "File", "Type", "Title", "Paragraph", "Subtitle"])

df.to_excel(str(Path(folder / r"TotalCircNew_No_IR_sortof.xlsx")))
