import numpy as np
import pandas as pd
from pathlib import Path
import re
from rapidfuzz import process, fuzz

homepath = str(Path.home())
print("The home path detected is {}.".format(homepath))

if r"C:\Users" in homepath:
    windows = True
    print("Detected Windows home path - using Jason's Dropbox folders")
    inputfolderroot = Path(r"C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification")
    outputfolder = inputfolderroot
else:
    windows = False
    print("Assuming Mercury home path - using Mercury folders")
    inputfolderroot = Path(r"/project/kh_mercury_1/CriCount/gvkeymerge_jason")
    outputfolder = inputfolderroot
    
inputfolder1 = Path(inputfolderroot / "Hassan")
inputfile1 = Path("Hassanfile_raw_updated2019030_truncated3.csv")
inputfolder2 = Path(inputfolderroot / "entryfiles_combined_v5")

inputfile2 = Path("entryfiles_combined_v5.xlsx")
compustatpdfolder = Path(inputfolderroot / "compustat_csv" / "ciqcompany_fragments")
outputfile = Path("Hassanfile_raw_updated2019030_truncated3_withcanonicalizednames.csv")
outputfilepath = Path(outputfolder / outputfile)


def read_file(inputfolder, inputfile, filetype="csv", inputfilepath=None, csv_header=False):
    if inputfilepath == None:
        inputfilepath = Path(inputfolder / inputfile)
    if filetype == "csv":
        if csv_header == False:
            return pd.read_csv(inputfilepath)
        else:
            return pd.read_csv(inputfilepath, header=csv_header)
    if filetype == "xlsx":
        return pd.read_excel(inputfilepath)
    
hassanpd = read_file(inputfolder1, inputfile1)

entryfilespd = read_file(inputfolder2, inputfile2, filetype="xlsx")
print(entryfilespd.duplicated("Title").sum())
entryfilespd = entryfilespd.drop_duplicates("Title")
print(entryfilespd.duplicated("Report").sum())

#%%
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

#%%
hassanpd, hassanpd_firmname, hassanname_dup = pd_firmname_clean(hassanpd, colname='company_name', conferencecall=False)
entryfilespd, entryfilespd_firmname, entryfilespd_dup = pd_firmname_clean(entryfilespd, colname="Title", conferencecall=True)

col_list = ['firm_name','exact_match','choice_h','sim_score_h','index_h']
firmname_hassanmatch = pd.DataFrame(np.zeros((len(entryfilespd_firmname), 5)), columns=col_list)
firmname_hassanmatch['firm_name'] = entryfilespd_firmname
#%%
# Exact match
def check_exact_match(base_df, checkagst_df):
    for row_index, entry_firmname in enumerate(base_df['firm_name']):
        for checkagst_firmname in checkagst_df:
            if entry_firmname == checkagst_firmname:
                base_df['exact_match'][row_index] += 1
                break
    return base_df

firmname_hassanmatch = check_exact_match(firmname_hassanmatch, hassanpd_firmname)

print(firmname_hassanmatch['exact_match'].sum())
#%%
#hassanmatch_1equals100 = firmname_hassanmatch
#hassanmatch_1equals100.to_csv(r'C:\Users\jasonjia\Dropbox\Projects\ConferenceCall\Output\FirmIdentification\hassanmatch_1equals100.csv')

def fuzzy_match(firmname_allmatches, firmname_hassanorcompustat, replaceifhigher=False):
    improvementlist_c = {}
    entrydf_firmname = firmname_allmatches['firm_name']
    for row_index, entry_firmname in enumerate(entrydf_firmname):
        if firmname_allmatches['exact_match'][row_index] == 0:
            res = process.extractOne(entrydf_firmname[row_index],firmname_hassanorcompustat,score_cutoff=90,processor=None) 
            print(res)
            if res != None:
                choice = firmname_allmatches.columns[2]
                sim_score = firmname_allmatches.columns[3]
                index = firmname_allmatches.columns[4]
                
                choice_current = firmname_allmatches[choice][row_index]
                sim_score_current = firmname_allmatches[sim_score][row_index]
                index_current = firmname_allmatches[index][row_index]
                choice_new = res[0]
                sim_score_new = res[1]
                index_new = res[2]
                
                if replaceifhigher == True and sim_score_current < sim_score_new and sim_score_current > 0:
                    improvement_c = str(choice_current) + ', ' + str(sim_score_current) + ', ' + str(index_current) \
                                  + " -> " + str(choice_new) + ', ' + str(sim_score_new) + ', ' + str(index_new) 
                    print(improvement_c)
                    improvementlist_c.append(improvement_c)
                    choice_current = choice_new
                    sim_score_current = sim_score_new
                    index_current = index_new
                if replaceifhigher == False:
                    choice_current = choice_new
                    sim_score_current = sim_score_new
                    index_current = index_new
                    
    return firmname_allmatches
        
#%%
firmname_hassanmatch = fuzzy_match(firmname_hassanmatch, hassanpd_firmname)

# Additional
hassanmatch_imperfectfirmnames = firmname_hassanmatch[firmname_hassanmatch['exact_match'] == 0]
hassanmatch_imperfectfirmnames = hassanmatch_imperfectfirmnames[hassanmatch_imperfectfirmnames['sim_score_h'] > 90]

#%%
col_list = ['firm_name','exact_match','choice_c','sim_score_c','index_c']
firmname_compustatmatch = pd.DataFrame(np.zeros((len(entryfilespd_firmname), 5)), columns=col_list)
firmname_compustatmatch['firm_name'] = firmname_hassanmatch['firm_name']
firmname_compustatmatch['exact_match'] = firmname_hassanmatch['exact_match']

#%%
for fragment in compustatpdfolder.iterdir():
    #frag_num_current = frag_num
    #print(fragment)
    frag_num = int(fragment.stem[-3:])
    if True: #frag_num >= frag_num_current:
        print(fragment.stem)
        if frag_num == 0:
            compustatpd_fragment = read_file(compustatpdfolder, fragment.name, filetype="csv")
        else:
            compustatpd_fragment = read_file(compustatpdfolder, fragment.name, filetype="csv", csv_header=None)
            compustatpd_fragment.columns =['companyid', 'companyname', 'countryid']
            compustatpd_fragment = string_clean(compustatpd_fragment['companyname'], removeallspaces=True)
        # firmname_compustatmatch = check_exact_match(firmname_compustatmatch, compustatpd_fragment)
        firmname_compustatmatch = fuzzy_match(firmname_compustatmatch, compustatpd_fragment, replaceifhigher=True)

        