#%%
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import random
from nltk.tokenize import sent_tokenize
from nltk.tokenize import wordpunct_tokenize
import re

# %%
os.chdir(r"/project/kh_mercury_1/CriCount2")
# os.chdir("C:/Users/jasonjia/Dropbox/ConferenceCall/Output/KeywordIdentification") # initially was sys.argv[1]

#%%
for i in range(1,11): # groups 1 to 10
    file_name = "group" + str(i) + "/" + "FR5.csv"
    try:
        raw_data = pd.read_csv(file_name)
    except FileNotFoundError:
        print("%s does not exist"%(file_name))
    if "total_data1" in vars():
        total_data1 = pd.concat([total_data1, raw_data], axis=0)
    else:
        total_data1 = raw_data



# %%
### reopen keywords ###
with open("keyterms.txt", "r", encoding="utf-8", errors="ignore") as f1:
    key_set = set(f1.read().splitlines())

keyw_list = list(key_set) 
keyw_list = [t.lower() for t in keyw_list]
var_list = ["Cri1"]
samples_call = pd.DataFrame({"Keywords":[], "Date":[], "Report":[], "File":[], "Type":[]})
for each_key in keyw_list:
    for each_var in var_list:
        if each_var == "Cri1":
            temp_data = total_data1[(total_data1[each_var]==1)]
        temp_data = temp_data.loc[:,["Date","Report","Keywords","File"]]
        temp_data = temp_data[temp_data["Keywords"]==each_key]
        temp_data["Type"] = each_var
        samples_call = pd.concat([samples_call,temp_data], axis=0)

# %%
def keyw_iden(keywords,sent):
    try:
        if isinstance(keywords,list):
            for each_keyword in keywords:
                if each_keyword in sent.replace("\n"," ").lower():
                    return True
        else:
            if keywords in sent.replace("\n"," ").lower():
                    return True
        return False
    except AttributeError:
        return False

### identify whether a word is fully a number (actually a percentage) ###
def num_iden(string):
    total_length = 0
    num_length = 0
    if "%" not in string:
        return False
    for char in string:
        if char not in '!%()*+,-./:;<=>?@[\\]^_`{|}~':
            total_length +=1
        if char in "0123456789":
            num_length += 1
    if total_length==num_length and total_length!=0:
        return True
    else:
        return False

### identify whether a total number word is inside a sentence ###
def num_contain(sent):
    tok_list = sent.split()
    for each_tok in tok_list:
        if num_iden(each_tok):
            return True
    return False

### identify whether the criteria is matched for each conference call ####
'''def identify_cost(call_script, check_len, keys_ident, behind=False):
    for i in range(len(call_script)):
        check_sent = call_script[i]
        if keyw_iden(keys_ident, check_sent):  ### a sentence contains a key word 
            end_index = min(i+check_len,len(call_script)-1)
            for t in range(i, end_index+1):
                if t==i and behind==True:
                    check_sent_part = check_sent.lower().split(keys_ident)[1]
                    if num_contain(check_sent_part):
                        return True
                    else:
                        continue
                if num_contain(call_script[t]):
                    return True
    return False'''

def identify_cost(check_sent, keys_ident, behind=False):
    if keyw_iden(keys_ident, check_sent):  ### a sentence contains a key word 
        if behind==True:
            check_sent_part = check_sent.replace("\n"," ").lower().split(keys_ident)[1]
            if num_contain(check_sent_part):
                return True
            else:
                return False
        if num_contain(check_sent):
            return True
    return False
'''
#### identify subsequent phrases ####
extra_list1 = ["is", "was", "are", "were", "has been"]
extra_list2 = ["increase to","increased to", "increases to","decrease to","decreased to", "decreases to","decrease from", "increase from","achieve","reach","decreases from", "increases from","decreased from","increased from","achieves","reaches","achieved","reached"]

#### def subsequent part (things from the list + percentage) ####
def identify_phrase(check_sent,key_ident,addi=False):
    if addi:
        check_list =  extra_list1 + extra_list2
    else:
        check_list = extra_list1
    if key_ident in check_sent.replace("\n"," ").lower():
        check_part = check_sent.replace("\n"," ").lower().split(key_ident)[1]
        for each_element in check_list:
            if each_element in check_part:
                check_part2 = check_part.split(each_element)
                if check_part2[1].split()!=[]:
                    key_num = check_part2[1].split()[0]
                    if check_part2[0] == " " and num_iden(key_num):
                        return True
    return False
'''

#### save the paragraph in the call with the keywords ###
#### paragraph are identified with space + \n ####
#### if not a clear paragraph is identified, choose the two sentences forward and afterward ####
def save_paragraph(keyword,call_script,check_len):
    paragraph_list = [t.replace("\n"," ") for t in re.split(r"\n\s*\n+",call_script) if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
    para_list = [t for t in call_script.split("\n") if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
    para_recon = " ".join(para_list)
    c_script = sent_tokenize(para_recon)
    for i in range(len(c_script)):
        check_sent = c_script[i]
        iden_status = False
        if check_len == 1:
            if identify_cost(check_sent,keyword,False):
                iden_status = True
        elif check_len == 2:
            if identify_cost(check_sent,keyword,True):
                iden_status = True            
        elif check_len == 3:
            if identify_phrase(check_sent, keyword, False):
                iden_status = True
        elif check_len == 4:
            if identify_phrase(check_sent, keyword, True):
                iden_status = True
    
        if iden_status:
            for w in range(len(paragraph_list)):
                if check_sent in paragraph_list[w]:
                    if w!=len(paragraph_list)-1:
                        return paragraph_list[w].replace("\n"," ") + " " + paragraph_list[w+1].replace("\n"," ")
                    else:
                        return paragraph_list[w].replace("\n"," ")
            basic_string = c_script[i-2] + " " + c_script[i-1] + " " + check_sent
            end_index = min(i+1,len(call_script)-1)
            for j in range(1,end_index-i+1):
                basic_string = basic_string + " " + c_script[i+j]
            return basic_string
    return "Nothing Found"    

#%%
samples_call.index = [t for t in range(samples_call.shape[0])]
#### the csv text raw ####
csv_dir1 = r"/project/kh_mercury_1/CriCount2"
csv_dir2 = r"/project/kh_mercury_1/CriCount2"

#csv_dir1 = r"C:/Users/jasonjia/Dropbox/ConferenceCall/Output/ConferenceCall/Csvtest"
#csv_dir2 = r"C:/Users/jasonjia/Dropbox/ConferenceCall/Output/ConferenceCall/Csvtest"


 
para_example = []
name = []
for i in range(samples_call.shape[0]):
    print(i)
    keyw = samples_call.loc[i]["Keywords"]
    file_name = samples_call.loc[i]["File"]
    report_num = samples_call.loc[i]["Report"]
    check_len = int(samples_call.loc[i]["Type"].replace("Cri",""))
    for i in range(1,11):
        filepathfound = False
        csv_dir_filepath = "/project/kh_mercury_1/CriCount2/group" + str(i) + "/" + file_name
        filepathfound = os.path.exists(csv_dir_filepath)
        if filepathfound == True:
            check_data = pd.read_csv(csv_dir_filepath)
    #except FileNotFoundError:
    #    check_data = pd.read_csv(csv_dir_filepath + "/" + file_name)
    call_script = check_data[check_data["Report"]==report_num]["Call"].values[0]
    para_example.append(save_paragraph(keyw,call_script,check_len))
    name.append(check_data[check_data["Report"]==report_num]["Title"].values[0])
samples_call["Title"] = name
samples_call["Paragraph"] = para_example
# %%
### save output ####
samples_call.to_excel("TotalCircnew.xlsx", index=None)


# %%
