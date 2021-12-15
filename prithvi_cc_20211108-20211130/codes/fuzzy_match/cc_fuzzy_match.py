import pandas as pd
import numpy as np
import os
import re
import string
from collections import Counter, defaultdict
from rapidfuzz import process, fuzz
import dask.dataframe as dd
import sys

df = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Filtered_Ordered_Amended_Correct_No_IR.csv")
df = df.rename({"Keyword": "Keywords", "Para": "Paragraph"}, axis = 1)
columns = ["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report"]
edf = pd.read_excel("entryfiles_combined_v5_withparagraphs.xlsx")

compustat_df = pd.read_csv("/project/kh_mercury_1/conference_call/output/03_firm_identification/03.3_compustat_processed_2/ciqcompany_mergedwithgvkeyandcountry.csv")
compustat_df = compustat_df[compustat_df["gvkey"].notnull()]
compustat_df

new_df = df[columns].rename({"final_gvkey": "gvkey", "final_country": "country"}, axis = 1)
new_df


df = pd.read_csv("Filtered_Ordered_Amended_Correct_No_IR.csv")
df = df.rename({"Keyword": "Keywords", "Para": "Paragraph"}, axis = 1)
columns = ["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report"]
#edf = pd.read_excel("entryfiles_combined_v5_withparagraphs_andgvkey.xlsx")
#edf

'''
edf_merge = edf.merge(compustat_df.drop_duplicates("gvkey"), on = "gvkey", how = "left")
edf_merge = edf_merge[["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report", "gvkey", "companyname", "country"]]
edf_merge

edf_merge.to_excel("old_conf_call_compustat_match.xlsx")
'''
combined = pd.concat([edf_merge, new_df])
combined

combined.to_excel("full_conf_calls_compustat_match.xlsx")

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

#full_df = pd.read_excel("updated_full_conf_calls_match.xlsx")
#full_df
df[df["Title"] == "nan"]

entry_df = pd.read_excel("entryfiles_combined_v5_withparagraphs_andgvkey.xlsx")
entry_df

def getTitles(row):
    if row["Title_x"] == "nan":#pd.isna(row["Title_x"]):
        return row["Title_y"]
    else:
        return row["Title_x"]

df = pd.read_excel("full_conf_calls_compustat_match.xlsx", engine = "openpyxl").drop("Unnamed: 0", axis = 1)
df["Title"] = df["Title"].astype(str)
full_df = df.copy()
full_df = full_df.merge(entry_df, on = ["Keywords", "Report"], how = "left")
full_df["Title"] = full_df.apply(getTitles, axis = 1)
full_df[full_df["Title"] == "nan"]

full_df

df, compustat_df = get_names(full_df, compustat_df, new_words)
df

df[df["Title"] == "nan"]

def parseResults(results):
    c_firms, sims = [], []
    for c_firm, sim, _  in results:
        c_firms.append(c_firm)
        sims.append(sim)
    return c_firms, sims

full_df = df.copy()
small = full_df
small_dask = dd.from_pandas(small, npartitions = 100)
match_choices = compustat_df["companyname_No_Punctuations"]
results = small_dask["Cleaned_Name_No_Punctuations"].apply(lambda x: process.extractOne(x, match_choices, scorer = fuzz.ratio), meta = "str")
results = results.compute(scheduler = "processes")

results

c_firms, sims = [], []
our_firms = full_df["Cleaned_Name_No_Punctuations"]
for our_firm, j in zip(our_firms, results):
    c_firm, sim = j[0], j[1]
    c_firms.append(c_firm)
    sims.append(sim)
full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match"] = c_firms
full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match_Similarity"] = sims
full_df

hassan_df = pd.read_csv("Hassanfile_raw_updated2019030_viewable.csv")
hassan_df = hassan_df[hassan_df["gvkey"].notnull()]
hassan_df = hassan_df[["gvkey", "company_name", "hqcountrycode", "ticker"]]
hassan_df = hassan_df.drop_duplicates("company_name")
hassan_df = hassan_df.reset_index(drop = True)
geo_df = pd.read_csv("ciqcountrygeo.csv")
non_null_geo_df = geo_df[geo_df["isocountry2"].notnull()]
country_dict = dict(non_null_geo_df.set_index("isocountry2")["country"])
hassan_df["country_name"] = hassan_df["hqcountrycode"].apply(lambda x: country_dict.get(x, np.nan))
hassan_df["company_name_No_Punctuations"] = hassan_df["company_name"].str.upper().str.split().apply(lambda x: remove_punc(x, new_words))
hassan_df

match_choices = hassan_df["company_name_No_Punctuations"]
results = small_dask["Cleaned_Name_No_Punctuations"].apply(lambda x: process.extractOne(x, match_choices, scorer = fuzz.ratio), meta = "str")
results = results.compute(scheduler = "processes")
c_firms, sims = [], []
our_firms = full_df["Cleaned_Name_No_Punctuations"]
for our_firm, j in zip(our_firms, results):
    c_firm, sim = j[0], j[1]
    c_firms.append(c_firm)
    sims.append(sim)
full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match"] = c_firms
full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match_Similarity"] = sims

c_gvkeys, c_countries = [], []
for i in full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match"]:
    subset = compustat_df[compustat_df["companyname_No_Punctuations"] == i]
    gvkey = subset["gvkey"].iloc[0]
    country = subset["country"].iloc[0]
    c_gvkeys.append(gvkey)
    c_countries.append(country)
full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match_gvkey"] = c_gvkeys
full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match_country"] = c_countries

h_gvkeys, h_countries = [], []
for i in full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match"]:
    subset = hassan_df[hassan_df["company_name_No_Punctuations"] == i]
    #display(subset)
    #break
    gvkey = subset["gvkey"].iloc[0]
    country = subset["country_name"].iloc[0]
    h_gvkeys.append(gvkey)
    h_countries.append(country)
full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match_gvkey"] = h_gvkeys
full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match_country"] = h_countries
full_df

def choose_gvkey(row, threshold = 95):
    s1 = "New_Cleaned_No_Punctuation_Compustat_Closest_Match_Similarity"
    s2 = "New_Cleaned_No_Punctuation_Hassan_Closest_Match_Similarity"
    
    if (row[s1] >= threshold) or (row[s2] >= threshold):
        if row[s1] >= row[s2]:
            gvkey = row["New_Cleaned_No_Punctuation_Compustat_Closest_Match_gvkey"]
            country = row["New_Cleaned_No_Punctuation_Compustat_Closest_Match_country"]
            return (gvkey, country)
        else:
            gvkey = row["New_Cleaned_No_Punctuation_Hassan_Closest_Match_gvkey"]
            country = row["New_Cleaned_No_Punctuation_Hassan_Closest_Match_country"]
            return (gvkey, country)
    
    else:
        return (np.nan, np.nan)

t = full_df.apply(choose_gvkey, axis = 1)
new_gvkeys = [i[0] for i in t]
new_countries = [i[1] for i in t]
full_df["final_gvkey"] = new_gvkeys
full_df["final_country"] = new_countries
full_df

full_df = full_df.rename({"Paragraph_x": "Paragraph", "Date_x": "Date", "Subtitle_x": "Subtitle"}, axis = 1)
full_df.columns

c_firms_fullnames, h_firms_fullnames = [], []
for c_firm, h_firm in zip(full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match"], full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match"]):
    c_subset = compustat_df[compustat_df["companyname_No_Punctuations"] == c_firm]
    h_subset = hassan_df[hassan_df["company_name_No_Punctuations"] == h_firm]
    c_fullname = c_subset["companyname"].iloc[0]
    h_fullname = h_subset["company_name"].iloc[0]
    c_firms_fullnames.append(c_fullname)
    h_firms_fullnames.append(h_fullname)
    
full_df["New_Cleaned_No_Punctuation_Compustat_Closest_Match_Fullname"] = c_firms_fullnames
full_df["New_Cleaned_No_Punctuation_Hassan_Closest_Match_Fullname"] = h_firms_fullnames
full_df

cols = ["Keywords", "Paragraph", "Date", "Title", "Subtitle", "Report",
       'Cleaned_Name', 'Cleaned_Name_No_Punctuations', 'New_Cleaned_No_Punctuation_Compustat_Closest_Match',
       'New_Cleaned_No_Punctuation_Compustat_Closest_Match_Similarity',
       'New_Cleaned_No_Punctuation_Compustat_Closest_Match_gvkey',
        "New_Cleaned_No_Punctuation_Compustat_Closest_Match_Fullname",
       'New_Cleaned_No_Punctuation_Compustat_Closest_Match_country', 
       'New_Cleaned_No_Punctuation_Hassan_Closest_Match',
       'New_Cleaned_No_Punctuation_Hassan_Closest_Match_Similarity',
       'New_Cleaned_No_Punctuation_Hassan_Closest_Match_gvkey',
        "New_Cleaned_No_Punctuation_Hassan_Closest_Match_Fullname",
       'New_Cleaned_No_Punctuation_Hassan_Closest_Match_country', 'final_gvkey', 'final_country']

new_full_df = full_df[cols]
new_names = []
for colname in new_full_df.columns:
    if colname[:4] == "New_":
        new_names.append(colname[4:])
    else:
        new_names.append(colname)
new_full_df.columns = new_names
new_full_df

new_matched = new_full_df[new_full_df["final_gvkey"].notnull()]
new_matched#.to_excel("updated_matched_conf_calls_match.xlsx", index = False)

new_unmatched = new_full_df[new_full_df["final_gvkey"].isnull()]
new_unmatched#.to_excel("updated_unmatched_conf_calls_match.xlsx", index = False)

filled_c = pd.read_excel("Filled_Updated_CC_Compustat_FuzzyMatchCandidates.xlsx")
filled_c = filled_c[filled_c["Correct"] == 1]
filled_c

filled_h = pd.read_excel("Filled_Updated_CC_Hassan_FuzzyMatchCandidates.xlsx")
filled_h = filled_h[filled_h["Correct"] == 1]
filled_h

comp_dict = dict(filled_c.set_index("CC Firm")["Compustat Firm"])
hassan_dict = dict(filled_h.set_index("CC Firm")["Hassan Firm"])

#drop_columns = ["new_gvkeys", "new_country", "final_gvkey", "final_country"]
#df = pd.read_excel("updated_full_conf_calls_match.xlsx")
df = new_full_df.copy()
types, closest_firms = [], []
for index, row in df.iterrows():
    gvkey = row["final_gvkey"]
    if not pd.isna(gvkey):
        types.append(np.nan)
        closest_firms.append(np.nan)
        continue
    
    cc_firm = row["Cleaned_Name_No_Punctuations"]
    comp_firm = comp_dict.get(cc_firm, -99999)
    if comp_firm == -99999:
        hassan_firm = hassan_dict.get(cc_firm, -99999)
        try:
            hassan_firm = hassan_firm.iloc[0]
        except:
            pass
        if hassan_firm == -99999:
            types.append(np.nan)
            closest_firms.append(np.nan)
        else:
            types.append("Hassan")
            closest_firms.append(hassan_firm)
    else:
        types.append("Compustat")
        closest_firms.append(comp_firm)

df["Manual_Match_Firm"] = closest_firms
df["Manual_Match_Type"] = types
df

gvkeys, countries, fullnames = [], [], []
for index, row in df.iterrows():
    final_gvkey = row["final_gvkey"]
    if not pd.isna(final_gvkey):
        gvkeys.append(final_gvkey)
        countries.append(row["final_country"])
        continue

    closest_firm = row["Manual_Match_Firm"]
    if pd.isna(closest_firm):
        gvkey, country, fullname = np.nan, np.nan, np.nan
    else:
        dataset = row["Manual_Match_Type"]
        if dataset == "Compustat":
            subset = compustat_df[compustat_df["companyname_No_Punctuations"] == closest_firm]
            gvkey, country, fullname = subset["gvkey"].iloc[0], subset["country"].iloc[0], subset["companyname"].iloc[0]
        elif dataset == "Hassan":
            subset = hassan_df[hassan_df["company_name_No_Punctuations"] == closest_firm]
            gvkey, country, fullname = subset["gvkey"].iloc[0], subset["country_name"].iloc[0], subset["company_name"].iloc[0]
    gvkeys.append(gvkey)
    countries.append(country)
    fullnames.append(fullname)

df["new_gvkeys"], df["new_country"] = gvkeys, country
df

gvkeys, countries, fullnames = [], [], []
for i in df["new_gvkeys"]:
    if pd.isna(i):
        gvkeys.append(np.nan)
        countries.append(np.nan)
        fullnames.append(np.nan)
        continue
    subset = compustat_df[compustat_df["gvkey"] == i]
    if len(subset) < 1:
        # Only Hassan Territory
        gvkeys.append(np.nan)
        countries.append(np.nan)
        fullnames.append(np.nan)
        continue
    gvkey, country, fullname = subset["gvkey"].iloc[0], subset["country"].iloc[0], subset["companyname"].iloc[0]
    gvkeys.append(i)
    countries.append(country)
    fullnames.append(fullname)
df["manual_gvkey"], df["manual_country"], df["manual_fullnames"] = gvkeys, countries, fullnames
df

drop_columns = ["new_gvkeys", "new_country", "final_gvkey", "final_country"]
rename_dict = {"manual_gvkey": "final_gvkey", "manual_country": "final_country", "manual_fullnames": "final_fullnames"}
df = df.drop(drop_columns, axis = 1)
df = df.rename(rename_dict, axis = 1)
df

df.to_excel("manual_full_updated_conf_calls.xlsx", index = False)

matched = df[df["final_gvkey"].notnull()]
matched#.to_excel("manual_matched_updated_conf_calls.xlsx", index = False)

unmatched = df[df["final_gvkey"].isnull()]
unmatched#.to_excel("manual_unmatched_updated_conf_calls.xlsx", index = False)