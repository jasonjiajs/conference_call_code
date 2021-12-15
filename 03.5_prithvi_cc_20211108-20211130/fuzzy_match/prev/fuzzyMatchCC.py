import pandas as pd
import dask.dataframe as dd
import numpy as np
import sys
import os
from rapidfuzz import fuzz, process

def get_relevant_info(title):
    if " - " in title:
        l = title.split(" - ")
        name_info = l[0]
        ticker_info = name_info.split()[-1].replace("(", "").replace(")", "")
        other_info = l[1]
        return name_info, ticker_info, other_info
    else:
        return title, np.nan, np.nan
    
def tickerBrackets(title):

    if " - " in title:
        l = title.split(" - ")
        name = l[0]
        t = name.split()[-1].replace("(", "").replace(")", "")
    else:
        name = title
        t = np.nan

    t_string = "({})".format(t)
    try:
        ind = name.index(t_string)
        cleansed_name = name[:(ind - 1)]
        return cleansed_name
    except:
        return name


def main():
    entity_df = pd.read_csv("Full_New_Not_Done.csv")
    entity_df = dd.from_pandas(entity_df, npartitions = 100, assume_missing = True)
    names = []
    tickers = []
    miscs = []
    entity_df["Title"] = entity_df["Title"].astype(str)
    for title in entity_df["Title"]:
        name, ticker, misc = get_relevant_info(title)
        names.append(name)
        tickers.append(ticker)
        miscs.append(misc)
    
    entity_df["Name"], entity_df["Ticker"], entity_df["Other Information"] = pd.Series(names), pd.Series(tickers), pd.Series(miscs)
    entity_df["Cleansed_Name"] = entity_df["Title"].apply(tickerBrackets, meta = "str")
    #entity_df["Cleansed_Name"] = entity_df.apply(lambda x: tickerBrackets(x["Name"], x["Ticker"]), axis = 1, meta = pd.Series)
    
    compustat_df = dd.read_csv("compustat_company_GVkey_ct.csv", assume_missing = True)
    compustat_df["Cleansed_Name"] = compustat_df["companyname"].str.upper()
    
    choices = compustat_df["Cleansed_Name"]
    results = entity_df["Cleansed_Name"].apply(lambda x: process.extractOne(x, choices, scorer=fuzz.ratio), meta = "str").to_frame()
    results = results.compute(scheduler = "processes")
    results.to_csv("CC_Compustat_Fuzzy_Match.csv")

if __name__ == "__main__":
    main()
