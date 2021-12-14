import pandas as pd
from pathlib import Path
path = Path(r"TotalCircNew_No_IR_sortof.xlsx")
df = pd.read_excel(path, engine = "openpyxl")
import numpy as np

columns = ['Keywords', 'Paragraph', 'Date', 'gvkey','Title','Subtitle','gvkey_h','gvkey_c','prob','gues_by_dticker','gues_name','countryid','Report','country','File']
df_res = pd.DataFrame(columns = columns)
df_res["Keywords"] = df["Keywords"]
df_res["Paragraph"] = df["Paragraph"]
df_res["Date"] = df["Date"]
df_res["Title"] = df["Title"]
df_res["Subtitle"] = df["Subtitle"]
df_res["Report"] = df["Report"]
df_res["File"] = df["File"]
df_res2 = df_res.replace(np.NaN,"")

df_res2.to_excel(r"cric1_newtotal_prithvi.xlsx", index=False)
