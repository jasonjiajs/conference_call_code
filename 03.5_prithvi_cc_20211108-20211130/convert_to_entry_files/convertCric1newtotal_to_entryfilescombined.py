import pandas as pd
from pathlib import Path
path = Path(r"/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/cric1_newtotal_prithvi.xlsx")
df = pd.read_excel(path, engine = "openpyxl")
import numpy as np

columns = ['Keywords', 'Paragraph', 'Date', 'gvkey','Title','Subtitle','Report']
df_res = df[columns]

df_res.to_excel(r"/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/entryfilescombined_test.xlsx", index=False)