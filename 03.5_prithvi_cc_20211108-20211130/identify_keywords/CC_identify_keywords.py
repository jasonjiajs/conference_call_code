import pandas as pd
import numpy as np
import os
from rapidfuzz import fuzz
from cleantext import clean
from collections import defaultdict
import re
import sys
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identify paragraphs with keywords showing up')
    parser.add_argument('inputfolder', help="input folder containing the .Hassan file.", type=str)
    parser.add_argument('outputfolder', help="input folder containing the .Hassan file.", type=str)
    parser.add_argument('keyterms_txt', help="location of the keyterms.txt file", type=str)
    args = parser.parse_args()
    inputfolder = Path(args.inputfolder)
    outputfolder = Path(args.outputfolder)
    keyterms_path = Path(args.keyterms_txt)

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

def main():
    keywords_df = pd.read_csv(keyterms_path, sep = "\t", header = None) # MANUAL # "/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.2_reference_files_2/keyterms.txt"
    keywords = keywords_df[0]
    
    for folder_num in range(1, 51):
        group = "group{}".format(folder_num)
        folder_fp = Path(inputfolder / group) # MANUAL # "/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.3_groups_test1/group{}"
        for file in os.listdir(folder_fp):
            if file == "FR5.csv": # MANUAL #
                continue
                
            file_fp = "{}/{}".format(folder_fp, file)
            cc_df = pd.read_csv(file_fp)
            dfs_list = []
            #dfs_list = cc_df.apply(lambda row: alt_keywords_from_one_call(row, keywords, clean = False), axis = 1)
            for index, row in cc_df.iterrows():
                temp = alt_keywords_from_one_call(row, keywords, clean = False, lower = True)
                dfs_list.append(temp)
            
            unclean_data = pd.concat(dfs_list).reset_index(drop = True)
            unclean_data = unclean_data.merge(cc_df, on = "Report", how = "left") 
            unclean_data["File"] = file
            unclean_data["HasNumber"] = unclean_data["Para"].apply(has_numbers)
            #unclean_data["ExtractedNumbers"] = unclean_data["Para"].apply(extractNumbers)
            #output_fp = "CriCount/Identified_Keywords/{}".format(file_fp)
            outdir = Path(outputfolder / group) # MANUAL # "/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/group{}".format(folder_num)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            output_fp = "{}/Full_Identified_{}.parquet.gzip".format(outdir, file) # MANUAL #
            unclean_data.to_parquet(output_fp, compression = "gzip")
            #unclean_data.to_csv("CriCount/Identified_Keywords/group1/{}".format(file))

if __name__ == "__main__":
    main()
