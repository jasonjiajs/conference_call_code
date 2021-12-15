import pandas as pd
import numpy as np
import os
from rapidfuzz import fuzz
from cleantext import clean
from collections import defaultdict
import re
import sys

def clean_str(s):
    t = s.replace("\\n", " ")
    t = t.replace("\\", "")
    if len(t) == 0:
        return ""
    if t[0] == '"':
        t = t[1:-1]
    return clean(t, fix_unicode = True, no_line_breaks = True, lower = False)

def alt_keywords_from_one_call(row, keywords, already_done_df, clean = True, lower = True):
    
    # This is an imperfect split, sometimes it breaks in the middle of a sentence
    call = str(row["Call"])
    paras_list = [t.replace("\n"," ") for t in re.split(r"\n\s*\n+", call) if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
    found_keywords, found_in_paras = [], []

    report_id = row["Report"]
    for para in paras_list:
        for keyword in keywords:
            done = False
            for para_2 in already_done_df["Paragraph"]:
                if check_n_prev_and_next(para, para_2, keyword, 5):
                    done = True
                    break
            if done == True:
                break
            
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
    try:
        start = p1.index(k)
    except:
        return False
    end = start + len(k)
    p1_start_chunk, p1_end_chunk = p1[:start], p1[end:]
    p2_start_chunk, p2_end_chunk = p2[:start], p2[end:]
    p1_preceding_n_words, p2_preceding_n_words = " ".join(p1_start_chunk.split()[inverted_n:]), " ".join(p2_start_chunk.split()[inverted_n:])
    p1_succeding_n_words, p2_succeding_n_words = " ".join(p1_end_chunk.split()[:n]), " ".join(p2_end_chunk.split()[:n])
    if (p1_preceding_n_words == p2_preceding_n_words) and (p1_succeding_n_words == p2_succeding_n_words):
        return True
    else:
        return False

def main():
    keywords_df = pd.read_csv("CriCount/keyterms.txt", sep = "\t", header = None)
    keywords = keywords_df[0]
    already_done_df = pd.read_parquet("CriCount/Master_Results.parquet.gzip").reset_index(drop = True)
    
    for folder_num in range(1, 51):
        folder_fp = "CriCount/group{}".format(folder_num)
        for file in os.listdir(folder_fp):
            if file == "FR5.csv":
                continue
                
            file_fp = "{}/{}".format(folder_fp, file)
            cc_df = pd.read_csv(file_fp)
            dfs_list = []
            #dfs_list = cc_df.apply(lambda row: alt_keywords_from_one_call(row, keywords, clean = False), axis = 1)
            for index, row in cc_df.iterrows():
                temp = alt_keywords_from_one_call(row, keywords, already_done_df, clean = False, lower = True)
                dfs_list.append(temp)
            
            unclean_data = pd.concat(dfs_list).reset_index(drop = True)
            #unclean_data = unclean_data.merge(cc_df, on = "Report", how = "left")
            unclean_data["File"] = file
            unclean_data["HasNumber"] = unclean_data["Para"].apply(has_numbers)
            #unclean_data["ExtractedNumbers"] = unclean_data["Para"].apply(extractNumbers)
            #output_fp = "CriCount/Identified_Keywords/{}".format(file_fp)
            outdir = "CriCount/Unique_Identified_Keywords/group{}".format(folder_num)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            output_fp = "{}/Unique_Identified_{}.parquet.gzip".format(outdir, file)
            unclean_data.to_parquet(output_fp, compression = "gzip")
            #unclean_data.to_csv("CriCount/Identified_Keywords/group1/{}".format(file))

if __name__ == "__main__":
    main()
