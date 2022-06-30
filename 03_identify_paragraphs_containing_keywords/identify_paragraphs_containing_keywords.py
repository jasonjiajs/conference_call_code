import pandas as pd
import numpy as np
import os
from cleantext import clean
from collections import defaultdict
import re
import sys
import argparse
from pathlib import Path

# Example command:
# python identify_paragraphs_containing_keywords.py C:\Users\jasonjia\Dropbox\Projects\conference_call\output\02_process_cc\02.2_csv_20210101_20220617 C:\Users\jasonjia\Dropbox\Projects\conference_call\output\03_identify_paragraphs_containing_keywords C:\Users\jasonjia\Dropbox\Projects\conference_call\code\03_identify_paragraphs_containing_keywords\reference_files\keywords.txt

# Parse arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identify paragraphs containing keywords')
    parser.add_argument('inputfolder', help="input folder containing the .csv files", type=str)
    parser.add_argument('outputfolder', help="output folder containing the paragraphs", type=str)
    parser.add_argument('keywords_filepath', help="filepath of the keywords.txt file", type=str)
    args = parser.parse_args()
    inputfolder = Path(args.inputfolder)
    outputfolder = Path(args.outputfolder)
    keywords_filepath = Path(args.keywords_filepath)

print("Input folder:", inputfolder)
print("Output folder:", outputfolder)
print("Keywords filepath:", keywords_filepath)

# Functions
def clean_str(s):
    t = s.replace("\\n", " ")
    t = t.replace("\\", "")
    if len(t) == 0:
        return ""
    if t[0] == '"':
        t = t[1:-1]
    return clean(t, fix_unicode = True, no_line_breaks = True, lower = False)

def alt_keywords_from_one_call(row, keywords, clean = True, lower = True):
    # This is an imperfect split, sometimes it breaks in the middle of a sentence
    call = str(row["Call"])
    paras_list = [t.replace("\n"," ") for t in re.split(r"\n\s*\n+", call) if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
    found_keywords, found_in_paras = [], []

    report_id = row["Report"]
    for para in paras_list:
        for keyword in keywords:
            if lower == True:
                para_lower = para.lower()
                keyword_lower = keyword.lower()
            if clean == True:
                para = clean_str(para)
            if lower == False:
                if keyword in para:
                    found_keywords.append(keyword)
                    found_in_paras.append(para)
            else:
                if keyword_lower in para_lower:
                    found_keywords.append(keyword)
                    found_in_paras.append(para)
    return pd.DataFrame({"Keyword": found_keywords, "Para": found_in_paras, "Report": report_id})

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def extractNumbers(text):
    digits = re.findall(r"[(\d.)]+", text)
    digits = [i for i in digits if i != "."]
    return digits

def check_n_prev_and_next(p1, p2, k, n = 5):
    inverted_n = n * -1 ### Good for indexing purposes
    start = p1.index(k)
    end = start + len(k)
    p1_start_chunk, p1_end_chunk = p1[:start], p1[end:]
    p2_start_chunk, p2_end_chunk = p2[:start], p2[end:]
    p1_preceding_n_words, p2_preceding_n_words = " ".join(p1_start_chunk.split()[inverted_n:]), " ".join(p2_start_chunk.split()[inverted_n:])
    p1_succeding_n_words, p2_succeding_n_words = " ".join(p1_end_chunk.split()[:n]), " ".join(p2_end_chunk.split()[:n])
    if (p1_preceding_n_words == p2_preceding_n_words) and (p1_succeding_n_words == p2_succeding_n_words):
        return True
    else:
        return False

# Main loop
keywords_df = pd.read_csv(keywords_filepath, sep = "\t", header = None)
keywords = keywords_df[0]

for file in os.listdir(inputfolder):    
    df_csv = pd.read_csv(file)
    df_combined = []
    for _, row in df_csv.iterrows():
        df = alt_keywords_from_one_call(row, keywords, clean = False, lower = True)
        df_combined.append(df)
    
    unclean_data = pd.concat(df_combined).reset_index(drop = True)
    unclean_data = unclean_data.merge(df, on = "Report", how = "left") 
    unclean_data["File"] = file
    unclean_data["HasNumber"] = unclean_data["Para"].apply(has_numbers)
    outputfilepath = Path(outputfolder / file)
    unclean_data.to_parquet(outputfilepath, compression = "gzip")
