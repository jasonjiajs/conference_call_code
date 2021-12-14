import pandas as pd
import numpy as np
from ast import literal_eval
from collections import defaultdict, Counter

df = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Duplicative_Amended_Correct_No_IR.csv")
df["Year"] = df["Date"].apply(pd.to_datetime).apply(lambda x: x.year)

keywords = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.2_reference_files_2/keyterms.txt", sep = "\t", header = None)

d = defaultdict(int)
d["hurdle rate"] = 5
d["cost of equity"] = 4
d["cost of capital"] = 3
d["IRR"] = 2
d["internal rate of return"] = 2
d["ROIC"] = 1
d["return on invested capital"] = 1
keywords["priority"] = keywords[0].apply(lambda x: d[x])
keywords = keywords[keywords[0] != "interest rate"]
keywords["lower"] = keywords[0].str.lower()
priority_dict = dict(keywords.set_index(0)["priority"])

def choose_according_to_priority(l, keywords_priority_dict):
    t = []
    if len(l) == 1:
        main_keyword = l[0]
    else:
        for k in l:
            t.append(keywords_priority_dict[k])
        highest_priority_index = pd.Series(t).idxmax()
        main_keyword = l[highest_priority_index]
    return main_keyword
df["List_Keywords"] = df["List_Keywords"].apply(literal_eval)
df["Highest_Priority_Keyword"] = df["List_Keywords"].apply(lambda x: choose_according_to_priority(x, priority_dict))
df["Keyword_Priority_Value"] = df["Highest_Priority_Keyword"].apply(lambda x: priority_dict[x])

df = df.sort_values("Keyword_Priority_Value", ascending = False)

df = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Duplicative_Amended_Correct_No_IR.csv")
df["DateObject"] = df["Date"].apply(pd.to_datetime)
df["Year"] = df["DateObject"].apply(lambda x: x.year)

def contains_percent(t):
    text = t.lower()
    to_keep = ["%", "per cent", "percent", "percentage"]
    for i in to_keep:
        if i in text:
            return True
    return False

# Tests
contains_percent("Hi, this is me.")
contains_percent("Hi, this % is me.")
contains_percent("Hello, I cannot say this. That's ridiculous")
contains_percent("Hello, I cannot say this. That's 100 Per Cent ridiculous")

df["Has%"] = df["Para"].apply(contains_percent)
df = df[df["Has%"] == True]

keywords = pd.read_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.2_reference_files_2/keyterms.txt", sep = "\t", header = None)
d = defaultdict(int)
d["hurdle rate"] = 5
d["cost of equity"] = 4
d["cost of capital"] = 3
d["IRR"] = 2
d["internal rate of return"] = 2
d["ROIC"] = 1
d["return on invested capital"] = 1
keywords["priority"] = keywords[0].apply(lambda x: d[x])
keywords = keywords[keywords[0] != "interest rate"]
keywords["lower"] = keywords[0].str.lower()
priority_dict = dict(keywords.set_index(0)["priority"])

def choose_according_to_priority(l, keywords_priority_dict):
    t = []
    if len(l) == 1:
        main_keyword = l[0]
    else:
        for k in l:
            t.append(keywords_priority_dict[k])
        highest_priority_index = pd.Series(t).idxmax()
        main_keyword = l[highest_priority_index]
    return main_keyword

df["List_Keywords"] = df["List_Keywords"].apply(literal_eval)
df["Highest_Priority_Keyword"] = df["List_Keywords"].apply(lambda x: choose_according_to_priority(x, priority_dict))
df["Keyword_Priority_Value"] = df["Highest_Priority_Keyword"].apply(lambda x: priority_dict[x])
df = df.sort_values("Keyword_Priority_Value", ascending = False)
df["Keyword_Older"] = df["Keyword"]
df["Keyword"] = df["Highest_Priority_Keyword"]

important_1 = ["hurdle rate", "cost of equity", "cost of capital"]
c1 = df["Year"] >= 2005
c2 = df["Year"] <= 2010
c3 = df["Keyword"].isin(important_1)
df_1 = df[(c1) & (c2) & (c3)]
df_1 = df_1.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

important_2 = ["hurdle rate", "cost of equity", "cost of capital"]
c1 = df["Year"] >= 2020
c2 = df["Keyword"].isin(important_2)
df_2 = df[(c1) & (c2)]
df_2 = df_2.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

other_years = [2001, 2002, 2003, 2004, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
important_3 = ["hurdle rate", "cost of equity", "cost of capital"]
c1 = df["Year"].isin(other_years)
c2 = df["Keyword"].isin(important_3)
df_3 = df[(c1) & (c2)]
df_3 = df_3.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

important_4 = ["IRR", "internal rate of return", "ROIC", "return on invested capital"]
c1 = df["Year"] >= 2005
c2 = df["Year"] <= 2010
c3 = df["Keyword"].isin(important_4)
df_4 = df[(c1) & (c2) & (c3)]
df_4 = df_4.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

important_5 = ["IRR", "internal rate of return", "ROIC", "return on invested capital"]
c1 = df["Year"] >= 2020
c2 = df["Keyword"].isin(important_5)
df_5 = df[(c1) & (c2)]
df_5 = df_5.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

other_years = [2001, 2002, 2003, 2004, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
important_6 = ["IRR", "internal rate of return", "ROIC", "return on invested capital"]
c1 = df["Year"].isin(other_years)
c2 = df["Keyword"].isin(important_6)
df_6 = df[(c1) & (c2)]
df_6 = df_6.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

df_7 = df[~(df.index.isin(df_1.index) | df.index.isin(df_2.index) | df.index.isin(df_3.index)
           |df.index.isin(df_4.index) | df.index.isin(df_5.index) | df.index.isin(df_6.index))]
df_7 = df_7.sort_values(["Highest_Priority_Keyword", "Title", "DateObject"], ascending = [False, True, True])

l = [df_1, df_2, df_3, df_4, df_5, df_6, df_7]
temp = pd.concat(l)

temp.to_csv("/project/kh_mercury_1/conference_call/output/04_keyword_identification/04.4_groups_keyword_test1/Filtered_Ordered_Amended_Correct_No_IR.csv", index = False)