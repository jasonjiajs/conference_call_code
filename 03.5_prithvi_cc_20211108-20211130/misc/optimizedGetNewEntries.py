import pandas as pd
import numpy as np
import os
from rapidfuzz import fuzz
from cleantext import clean
from collections import defaultdict
import re
import sys

def check_n_prev_and_next(p1, p2, k, n = 5):
    inverted_n = n * -1 ### Good for indexing purposes
    try:
        start = p1.index(k)
    except:
        start = p1.lower().index(k.lower())
    end = start + len(k)
    p1_start_chunk, p1_end_chunk = p1[:start], p1[end:]
    p2_start_chunk, p2_end_chunk = p2[:start], p2[end:]
    p1_preceding_n_words, p2_preceding_n_words = " ".join(p1_start_chunk.split()[inverted_n:]), " ".join(p2_start_chunk.split()[inverted_n:])
    p1_succeding_n_words, p2_succeding_n_words = " ".join(p1_end_chunk.split()[:n]), " ".join(p2_end_chunk.split()[:n])
    if (p1_preceding_n_words == p2_preceding_n_words) and (p1_succeding_n_words == p2_succeding_n_words):
        return True
    else:
        return False

def apply_to_each_row(row, paras_2, n):
    para_1, keyword_1 = row["Para"], row["Keyword"]
    for para_2 in paras_2:
        if check_n_prev_and_next(para_1, para_2, keyword_1, n = 5):
            already_done_paras.append(para_1)
    
def main():
    
    our_df = pd.read_csv("Full_Master_Keywords.csv").reset_index(drop = True)
    our_df = our_df[our_df["HasNumber"] == True]
    #already_done_df = pd.read_parquet("Master_Results.parquet.gzip").reset_index(drop = True)
    already_done_df = pd.read_excel("entryfiles_combined_v5_withparagraphs.xlsx", engine = "openpyxl")
    
    #
    #common = set(already_done_df["Report"]).intersection(set(our_df["Report"]))
    #our_df = our_df[our_df["Report"].isin(common)].iloc[:10000]
    #already_done_df = already_done_df[already_done_df["Report"].isin(common)].iloc[:10000]
    
    already_done_paras = []
    for para_1, keyword_1, report_1 in zip(our_df["Para"], our_df["Keyword"], our_df["Report"]):
        subset = already_done_df[already_done_df["Report"] == report_1]
        for para_2 in subset["Paragraph"]:
            if check_n_prev_and_next(para_1, para_2, keyword_1, n = 5):
                already_done_paras.append(para_1)
                break
    
    not_done_df = our_df[~(our_df["Para"].isin(already_done_paras))]
    not_done_df.to_csv("Full_New_Not_Done.csv")
    
if __name__ == "__main__":
    main()
