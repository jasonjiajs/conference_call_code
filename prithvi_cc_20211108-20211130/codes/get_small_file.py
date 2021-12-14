import pandas as pd
import numpy as np
import os
import sys

def main():
    #comp_merge_df = pd.read_csv("CC_CompustatMerge.csv")
    #t1 = comp_merge_df.iloc[:1000]
    #t1.to_csv("Small_CC_CompustatMerge.csv")
    
    hassan_merge_df = pd.read_csv("CC_HassanMerge.csv")
    t2 = hassan_merge_df.iloc[:500]
    t2.to_csv("New_Small_CC_HassanMerge.csv")
    
    t3 = pd.read_csv("Full_New_Not_Done.csv")
    3 = t3[t3["Keyword"] != "interest rate"]
    t3.to_csv("No_IR.csv")
    t3.iloc[:1000].to_csv("Small_No_IR.csv")

if __name__ == "__main__":
    main()
