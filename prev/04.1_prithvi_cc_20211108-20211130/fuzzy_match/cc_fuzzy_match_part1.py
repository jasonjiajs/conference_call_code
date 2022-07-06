import pandas as pd
import numpy as np
import os
import re
import string
from collections import Counter, defaultdict
from rapidfuzz import process, fuzz
import dask.dataframe as dd
import sys
from pathlib import Path

# folder = Path("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1")
df = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Filtered_Ordered_Amended_Correct_No_IR.csv")
new_df = df.rename({"Keyword": "Keywords", "Para": "Paragraph"}, axis = 1)
columns = ["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report"]
new_df = new_df[columns].rename({"final_gvkey": "gvkey", "final_country": "country"}, axis = 1)

compustat_df = pd.read_csv("/project/kh_mercury_1/conference_call/output/03_firm_identification/03.3_compustat_processed_2/ciqcompany_mergedwithgvkeyandcountry.csv")
compustat_df = compustat_df[compustat_df["gvkey"].notnull()]

edf = pd.read_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/entryfilescombined_test.xlsx", engine = "openpyxl")
edf_merge = edf.merge(compustat_df.drop_duplicates("gvkey"), on = "gvkey", how = "left")
edf_merge = edf_merge[["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report", "gvkey", "companyname", "country"]]

edf_merge.to_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/old_conf_call_compustat_match.xlsx")

combined = pd.concat([edf_merge, new_df])

combined.to_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/full_conf_calls_compustat_match.xlsx")