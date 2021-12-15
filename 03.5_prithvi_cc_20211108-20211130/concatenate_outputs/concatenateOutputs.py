import pandas as pd
import numpy as np
import os
from rapidfuzz import fuzz
from cleantext import clean
from collections import defaultdict
import re
import sys

def main():
    
    ### Already Done
    #dfs_list = []
    #for i in os.listdir("Entry files"):
    #    fp = "Entry files/" + i
    #    df = pd.read_excel(fp, engine = "openpyxl", skiprows = [0])
    #    dfs_list.append(df)
    #master_df = pd.concat(dfs_list)
    #master_df.to_parquet("Master_Results.parquet.gzip", compression = "gzip")
    
    ### Ours:
    dfs_list = []
    group_numbers = range(1, 51)
    for group_num in group_numbers:
        fp = "/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/group{}/".format(group_num) ## MANUAL ##
        # Full_Identified_Keywords/
        for f in os.listdir(fp):
            file_fp = fp + f
            df = pd.read_parquet(file_fp)
            dfs_list.append(df)
    master_df = pd.concat(dfs_list)
    master_df.to_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Full_Master_Keywords.csv") ## MANUAL ##
    master_df.to_parquet("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Full_Master_Keywords.parquet.gzip", compression = "gzip") ## MANUAL ##
    
if __name__ == "__main__":
    main()
