import numpy as np
import pandas as pd
from pathlib import Path
import re
import sys
import os
from rapidfuzz import process, fuzz
import dask.dataframe as dd

# equivalent to preparename function in original julia file

def string_clean(pd, removeallspaces=False):
    ''' converts a df column into lower case, removes special characters '''
    pd_clean = pd.str.lower()
    if removeallspaces == False:
        nonwords_retainspaces = re.compile("[^a-zA-Z\d\s]")  
        pd_clean = pd_clean.replace(nonwords_retainspaces, "")
        morethanonespace = re.compile("\s{2+}")
        pd_clean = pd_clean.replace(morethanonespace, " ")
    else:
        nonwords_removespaces = re.compile("\W")  
        pd_clean = pd_clean.replace(nonwords_removespaces, "")
    pd_clean = pd_clean.str.strip()
    return pd_clean

words_to_remove = ["group","plc","ltd","limited","ag","corp","corporation",
                   "incorporation","laboratories","labs","the",
                   "holdings","oyj","inc","co","and", "company","trust","investment",
                   "investments","sln","sa", "spa", "llc", "as", "asa"]

words_to_remove_conferencecall = ["event transcript of", "event brief of", "earnings conference call","conference call on productivity", 
       "earnings release conference", "financial release conference", "conference call regarding", 
       "earnings conference", "comprehensive review", "final transcript", "edited transcript", 
       "week conference", "conference call", "edited brief", "preliminary brief", "earnings call", 
       "earning call", "preliminary transcript", "final transcript", "call","cal","merger","c",
       "earning","earnings", "to discuss","jan","feb","mar","apr","may","jun","jul","aug","sep",
       "oct","nov","dec", "conference", "quarter","st","nd","rd","th", "q1", "q2", "q3", "q4",
       "proposed","propose", "transc", "final","preliminary"]

def remove_words(df, words_to_remove, conferencecall):
    lst = [" " + entry + " " for entry in df]
    for word_to_remove in words_to_remove:
        regex = re.compile(" " + word_to_remove + " ")
        lst = [re.sub(regex, " ", entry) for entry in lst]
    if conferencecall == True:
        for word_to_remove in words_to_remove_conferencecall:
            regex = re.compile(" " + word_to_remove + " ")
            lst = [re.sub(regex, " ", entry) for entry in lst]
        regex_year = re.compile("\s+[0-9]{4}\s+")
        lst = [re.sub(regex_year, " ", entry) for entry in lst]
                                
    df_res = pd.Series(lst)
    df_res.str.strip()
    df_res_dup = df_res[df_res.duplicated()] # print duplicates
    return df_res, df_res_dup

def pd_firmname_clean(df, colname, conferencecall):    
    df_clean = df[colname]
    df_clean = string_clean(df_clean, removeallspaces=False)
    df_clean, df_clean_dup = remove_words(df_clean, words_to_remove, conferencecall)
    df_clean_nospaces = string_clean(df_clean, removeallspaces=True)
    df['company_name_cleaned'] = df_clean
    df['company_name_cleaned_nospaces'] = df_clean_nospaces
    return df, df_clean_nospaces, df_clean_dup

def get_gvkey_and_name(df, cleaned_name, hassan = True):
    subset = df[df["company_name_cleaned"] == cleaned_name]
    if hassan:
        fullname = subset["company_name"].iloc[0]
        gvkey = subset["gvkey"].iloc[0]
    else:
        fullname = subset["companyname"].iloc[0]
        gvkey = subset["gvkey"].iloc[0]
    return gvkey, fullname

def main():
    keyword_df = pd.read_csv("Filtered_Ordered_Amended_Correct_No_IR.csv")
    hassan_df = pd.read_csv("Hassanfile_raw_updated2019030_truncated3.csv")
    compustat_df = pd.read_csv("compustat_company_GVkey_ct.csv")
    
    ### Clean the datasets
    keyword_df_clean, b, c = pd_firmname_clean(keyword_df, colname="Title", conferencecall=True)
    hassan_df_clean, b, c = pd_firmname_clean(hassan_df, colname='company_name', conferencecall=False)
    compustat_df_clean, b, c = pd_firmname_clean(compustat_df, colname="companyname", conferencecall=False)
    
    ### Merge with Hassan
    hassan_merged = keyword_df_clean.merge(hassan_df_clean, on = "company_name_cleaned")
    hassan_merged.to_csv("CC_Hassan_Merged.csv")
    
    ### Merge with Compustat
    comp_merged = keyword_df_clean.merge(compustat_df_clean, on = "company_name_cleaned")
    comp_merged.to_csv("CC_Compustat_Merged.csv")
    
    ### Making it a dask dataframe
    keyword_df_clean = dd.from_pandas(keyword_df_clean, npartitions = 100)
    
    ### Fuzzy Match with Hassan
    hassan_choices = hassan_df_clean["company_name_cleaned"]
    results = keyword_df_clean["company_name_cleaned"].apply(lambda x: process.extractOne(x, hassan_choices, scorer = fuzz.ratio), meta = "str")
    results = results.compute(scheduler = "processes")
    hassan_cleaned_names = [i[0] for i in results]
    hassan_cleaned_names_similarities = [i[1] for i in results]
    
    hassan_gvkeys, hassan_names = [], []
    for c_name in hassan_cleaned_names:
        gvkey, name = get_gvkey_and_name(hassan_df_clean, c_name, True)
        hassan_gvkeys.append(gvkey)
        hassan_names.append(name)
    #results.to_csv("CC_Hassan_Fuzzy_Match.csv")
    
    ### Fuzzy Match with Compustat
    compustat_choices = compustat_df_clean["company_name_cleaned"]
    results = keyword_df_clean["company_name_cleaned"].apply(lambda x: process.extractOne(x, compustat_choices, scorer = fuzz.ratio), meta = "str")
    results = results.compute(scheduler = "processes")
    compustat_cleaned_names = [i[0] for i in results]
    compustat_cleaned_names_similarities = [i[1] for i in results]
    
    compustat_gvkeys, compustat_names = [], []
    for c_name in compustat_cleaned_names:
        gvkey, name = get_gvkey_and_name(compustat_df_clean, c_name, False)
        compustat_gvkeys.append(gvkey)
        compustat_names.append(name)
    #results.to_csv("CC_Compustat_Fuzzy_Match.csv")
    
    # Going back to a pandas DF:
    keyword_df_clean = keyword_df_clean.compute(scheduler = "processes")
    
    # Adding Hassan Fuzzy Match Info
    keyword_df_clean["Hassan_Closest_Match"] = hassan_cleaned_names
    keyword_df_clean["Hassan_Closest_Match_Similarity"] = hassan_cleaned_names_similarities
    #keyword_df_clean["Hassan_Closest_Match_Fullname"], keyword_df_clean["Hassan_Closest_Match_gvkey"] = keyword_df_clean["Hassan_Closest_Match"].apply(lambda x: get_gvkey_and_name(compustat_df_clean, x, False))
    keyword_df_clean["Hassan_Closest_Match_Fullname"] = hassan_names
    keyword_df_clean["Hassan_Closest_Match_gvkey"] = hassan_gvkeys
    
    # Adding Compustat Fuzzy Match Info
    keyword_df_clean["Compustat_Closest_Match"] = compustat_cleaned_names
    keyword_df_clean["Compustat_Closest_Match_Similarity"] = compustat_cleaned_names_similarities
    #keyword_df_clean["Compustat_Closest_Match_Fullname"], keyword_df_clean["Compustat_Closest_Match_gvkey"] = keyword_df_clean["Compustat_Closest_Match"].apply(lambda x: get_gvkey_and_name(compustat_df_clean, x, False))
    keyword_df_clean["Compustat_Closest_Match_Fullname"] = compustat_names
    keyword_df_clean["Compustat_Closest_Match_gvkey"] = compustat_gvkeys
    
    keyword_df_clean.to_csv("FuzzyMatched_Ordered_Filtered_Amended_No_IR.csv")
    
if __name__ == "__main__":
    main()
