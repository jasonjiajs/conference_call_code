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

entry_df = pd.read_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/entryfilescombined_test.xlsx", engine = "openpyxl")

entry_df.to_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/entryfilescombined_test2.xlsx")

entry_df2 = pd.read_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/entryfilescombined_test2.xlsx", engine = "openpyxl")

def getTitles(row):
    if row["Title_x"] == "nan":#pd.isna(row["Title_x"]):
        return row["Title_y"]
    else:
        return row["Title_x"]

df = pd.read_excel("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/full_conf_calls_compustat_match.xlsx", engine = "openpyxl").drop("Unnamed: 0", axis = 1)


print("done")