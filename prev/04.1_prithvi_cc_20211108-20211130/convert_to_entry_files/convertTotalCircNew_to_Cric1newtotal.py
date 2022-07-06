import pandas as pd
from pathlib import Path
path = Path(r"/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/TotalCircNew_No_IR_sortof.xlsx")
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

df_res2.to_excel(r"/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/cric1_newtotal_prithvi.xlsx", index=False)
