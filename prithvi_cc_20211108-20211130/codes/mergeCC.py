import pandas as pd
import numpy as np
import sys
import os

def get_relevant_info(title):
    if " - " in title:
        l = title.split(" - ")
        name_info = l[0]
        ticker_info = name_info.split()[-1].replace("(", "").replace(")", "")
        other_info = l[1]
        return name_info, ticker_info, other_info
    else:
        return title, np.nan, np.nan
    
def tickerBrackets(name, t):
    t_string = "({})".format(t)
    try:
        ind = name.index(t_string)
        cleansed_name = name[:(ind - 1)]
        return cleansed_name
    except:
        return name

def main():
    entity_df = pd.read_csv("Full_New_Not_Done.csv")
    
    names = []
    tickers = []
    miscs = []
    entity_df["Title"] = entity_df["Title"].astype(str)
    for title in entity_df["Title"]:
        name, ticker, misc = get_relevant_info(title)
        names.append(name)
        tickers.append(ticker)
        miscs.append(misc)
    
    entity_df["Name"], entity_df["Ticker"], entity_df["Other Information"] = names, tickers, miscs
    entity_df["Cleansed_Name"] = entity_df.apply(lambda x: tickerBrackets(x["Name"], x["Ticker"]), axis = 1)
    compustat_df = pd.read_csv("compustat_company_GVkey_ct.csv")
    compustat_df["Cleansed_Name"] = compustat_df["companyname"].str.upper()
    compustat_merge = entity_df.merge(compustat_df, on = "Cleansed_Name")
    compustat_merge.to_csv("CC_CompustatMerge.csv")
    
    hassan_df = pd.read_csv("Hassanfile_raw_updated2019030_truncated3.csv")
    hassan_df["Cleansed_Name"] = hassan_df["company_name"].str.upper()
    hassan_merge = hassan_df.merge(entity_df, on = "Cleansed_Name")
    hassan_merge.to_csv("CC_HassanMerge.csv")
    
if __name__ == "__main__":
    main()
    
