import pandas as pd
import numpy as np
import os
import sys
from collections import defaultdict, Counter

df = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Full_Master_Keywords.csv")
# Previously "Full_New_Not_Done.csv", because that filtered out the ones that appeared in the first search.
df = df[df["Keyword"] != "interest rate"]
correct = []
para_counts = []
count = 0
for keyword, para in zip(df["Keyword"], df["Para"]):
    keyword, para = keyword.lower(), para.lower()
    try:
        start = para.index(keyword)
        end = start + len(keyword)
    except:
        count += 1
        continue
    
    if start == 0:
        full_keyword = keyword + " "
    elif end == len(para) - 1:
        full_keyword = " " + keyword
    else:
        full_keyword = " " + keyword + " "
    
    
    correct.append(full_keyword in para)
    num_counts = para.count(full_keyword)
    para_counts.append(num_counts)

df["Correct"] = correct
df["NumberOfOccurences"] = para_counts
final_df = df[df["Correct"] == 1]

para_dict = defaultdict(list)
for para in final_df["Para"].unique():
    subset = final_df[final_df["Para"] == para]
    para_dict[para].append(list(subset["Keyword"]))
final_df["List_Keywords"] = final_df["Para"].apply(lambda x: list(set((para_dict[x])[0])))
#final_df = final_df.drop_duplicates("Para")
final_df.to_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Duplicative_Amended_Correct_No_IR.csv")
