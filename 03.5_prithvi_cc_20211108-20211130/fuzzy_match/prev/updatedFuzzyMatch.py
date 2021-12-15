import pandas as pd
import numpy as np
import os
import re
import string
from collections import Counter, defaultdict
from rapidfuzz import process, fuzz
import dask.dataframe as dd
import sys

df = pd.read_excel("full_conf_calls_compustat_match.xlsx", engine = "openpyxl").drop("Unnamed: 0", axis = 1)
df["Title"] = df["Title"].astype(str)
compustat_df = pd.read_csv("ciqcompany_mergedwithgvkeyandcountry.csv")
compustat_df = compustat_df[compustat_df["gvkey"].notnull()]

old_words = ["earnings conference call","conference call on productivity", "earnings release conference", "financial release conference",
        "conference call regarding", "earnings conference", "comprehensive review", "final transcript", "edited transcript",
        "week conference", "conference call", "edited brief", "preliminary brief", "earnings call", "earning call",
        "preliminary transcript", "final transcript", "call","cal","merger","c", "earning","earnings", "to discuss",
        "group","plc","ltd","limited","ag","corp","corporation","Incorporation","laboratories","labs","the","proposed","propose",
        "holdings","oyj","inc","conference","co", "final","preliminary","and","&",
        "company","trust","investment","investments","sln","sa","s.p.a.","spa","transc", "quarter","st","nd","rd","th",
        "q", "jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
to_remove = ["cal", "c", "and", "&", "st", "nd", "rd", "th", "q"]
new_words = list(set(old_words) - set(to_remove))
new_words = [i.upper() for i in new_words]

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
    
def remove_punc(words, l):
    no_punc_words = [s.translate(str.maketrans("", "", string.punctuation)) for s in words]
    return " ".join(no_punc_words)

def remove_punctuations_and_words(words, l):
    no_punc_words = [s.translate(str.maketrans("", "", string.punctuation)) for s in words]
    filtered = [i for i in no_punc_words if i not in l]
    return " ".join(filtered)
    
def get_names(df, compustat_df, new_words):
    names = []
    tickers = []
    miscs = []
    for title in df["Title"]:
        name, ticker, misc = get_relevant_info(title)
        names.append(name)
        tickers.append(ticker)
        miscs.append(misc)
    
    df["Name"], df["Ticker"], df["Other Information"] = names, tickers, miscs
    df["Cleaned_Name"] = df.apply(lambda x: tickerBrackets(x["Name"], x["Ticker"]), axis = 1)
    df["Cleaned_Name_No_Punctuations"] = df["Cleaned_Name"].str.split().apply(lambda x: remove_punc(x, new_words))
    df["Cleaned_Name_No_Punctuations_And_Removed_Words"] = df["Cleaned_Name"].str.split().apply(lambda x: remove_punctuations_and_words(x, new_words))
    
    compustat_df["companyname_No_Punctuations"] = compustat_df["companyname"].str.upper().str.split().apply(lambda x: remove_punc(x, new_words))
    compustat_df["companyname_No_Punctuations_And_Removed_Words"] = compustat_df["companyname"].str.upper().str.split().apply(lambda x: remove_punctuations_and_words(x, new_words))
    return df, compustat_df

df, compustat_df = get_names(df, compustat_df, new_words)

def parseResults(results):
    c_firms, sims = [], []
    for c_firm, sim, _  in results:
        c_firms.append(c_firm)
        sims.append(sim)
    return c_firms, sims

def performFuzzyMatch(df, compustat_df):
    small_dask = dd.from_pandas(df, npartitions = 100)
    
    ### For cleaned name
    match_choices = compustat_df["companyname"]
    results = small_dask["Cleaned_Name"].apply(lambda x: process.extractOne(x, match_choices, scorer = fuzz.ratio), meta = "str")
    results = results.compute(scheduler = "processes")
    c_firms, sims = parseResults(results)
    output_col_name = "Cleaned_Compustat_Closest_Match"
    df[output_col_name], df[("{}_Similarity".format(output_col_name))] = c_firms, sims
    
    ### For removed punctuations
    match_choices = compustat_df["companyname_No_Punctuations"]
    results = small_dask["Cleaned_Name_No_Punctuations"].apply(lambda x: process.extractOne(x, match_choices, scorer = fuzz.ratio), meta = "str")
    results = results.compute(scheduler = "processes")
    c_firms, sims = parseResults(results)
    output_col_name = "Cleaned_No_Punctuation_Compustat_Closest_Match"
    df[output_col_name], df[("{}_Similarity".format(output_col_name))] = c_firms, sims
    
    ### For removed punctuations and words
    match_choices = compustat_df["companyname_No_Punctuations_And_Removed_Words"]
    results = small_dask["Cleaned_Name_No_Punctuations_And_Removed_Words"].apply(lambda x: process.extractOne(x, match_choices, scorer = fuzz.ratio), meta = "str")
    results = results.compute(scheduler = "processes")
    c_firms, sims = parseResults(results)
    output_col_name = "Cleaned_No_Punctuation_And_Removed_Words_Compustat_Closest_Match"
    df[output_col_name], df[("{}_Similarity".format(output_col_name))] = c_firms, sims
    return df

final_df = performFuzzyMatch(df, compustat_df)
final_df.to_excel("CC_CompustatFuzzyMatchTrial.csv")
