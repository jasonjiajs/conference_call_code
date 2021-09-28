#### this file serves to count the number of conference calls with keywords ###

#%%
import csv
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import wordpunct_tokenize
import os
import pandas as pd
import sys
import re


csv_dir = "/project/kh_mercury_1/CriCount2/" 

#"/project/kh_mercury_1/CriCount2/" # initially was sys.argv[1]
target_dir = "/project/kh_mercury_1/CriCount2/" 

#"/project/kh_mercury_1/CriCount2/" # initially was sys.argv[2]



#%%
#####　add any keywords in the text file ####
with open("keyterms.txt", "r", encoding="utf-8", errors="ignore") as f1:

    key_set = set(f1.read().splitlines())

keyw_list = list(key_set) 
keyw_list = [t.lower() for t in keyw_list]

#%%
### identify whether there is a keyword in a paragraph ###
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

### identify whether a total number is inside a sentence ###
def num_contain(sent):
    tok_list = sent.split()
    for each_tok in tok_list:
        if num_iden(each_tok):
            return True
    return False

### identify whether the criteria is matched for each conference call ####
###  check_len means the number of subsequent/forward sentences to look for a number ###
### if check_len = 0, meaning just focus on the sentence with keywords ###
### behind = True if only find number in subsequent sentences ####
### call_script is a list of sentences ######
def identify_cost(call_script, check_len, keys_ident, behind=False):  
    for i in range(len(call_script)):
        check_sent = call_script[i]   ### check keywords by sentence ####
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
    return False


#### identify the total conference_call by the same rule as identify_cost  ####
#### conf_call is the raw long string of a call script ####
#### the function simply reconstruct the string by getting rid of the paragraph delimiter and page number ####
def identify_total(conf_call, check_len, keys_ident, behind=False):
    try:
        para_list = [t for t in conf_call.split("\n") if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
        para_recon = " ".join(para_list)
    except AttributeError:
        return False
    return identify_cost(sent_tokenize(para_recon), check_len, keys_ident,behind)


'''
#### identify subsequent phrases ####
extra_list1 = ["is", "was", "are", "were", "has been"]
extra_list2 = ["increase to","increased to", "increases to","decrease to","decreased to", "decreases to","decrease from", "increase from","achieve","reach","decreases from", "increases from","decreased from","increased from","achieves","reaches","achieved","reached"]

#### def subsequent part (things from the list + percentage) ####
def identify_phrase(conf_call,key_ident,addi=False):
    try:
        para_list = [t for t in conf_call.split("\n") if len(t)>0 and not re.match(r"^\s*[0-9]+$",t)]
        para_recon = " ".join(para_list)
    except AttributeError:
        return False
    call_script = sent_tokenize(para_recon)
    if addi:
        check_list =  extra_list1 + extra_list2
    else:
        check_list = extra_list1
    for i in range(len(call_script)):
        check_sent = call_script[i]
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
#%% 
##### form a raw file containing which file contains which keyword
##### if a call contains several keywords, it will appear more than once ####
total_data = pd.DataFrame({"Date":[], "Report":[], "Keywords":[], "Cri1":[], "File":[]})


# %%
### read data now ####   
### csv_dir is passed in by the submit script file ####
for i in range(1,11):
    foldername = "group" + str(i)
    csv_dir_group = csv_dir + foldername
    target_dir_group = target_dir + foldername
    print(csv_dir_group)
    os.chdir(csv_dir_group)
    csv_list = os.listdir(csv_dir_group)

###"Cri2":[], "Cri3":[],"Cri4":[], "File":[]})
    for each_csv in csv_list:
        if ("CC_List" in each_csv) | (each_csv[-4:]!=".csv") | (each_csv[-7:]=="FR5.csv"): # don't run code if the document is CC_List. Run if it's not - i.e. if it's the processed csv file actually containing the call.
            continue #to check for next file in csv_list
        file_csv = csv_dir_group + "/" + each_csv
        print(file_csv)
        data_frame = pd.read_csv(file_csv)
        data_frame = data_frame[["Date","Report","Call"]]
        for each_key in keyw_list:
            temp_data = data_frame[["Date","Report"]]
            if isinstance(each_key,list):
                temp_data["Keywords"] = each_key[0] + "/" + each_key[1]
            else:
                temp_data["Keywords"] = each_key
            temp_data["Cri1"] = data_frame.apply(lambda x: identify_total(x.Call,0,each_key,False), axis=1)
            ##temp_data["Cri2"] = data_frame.apply(lambda x: identify_total(x.Call,0, each_key,True), axis=1)
            ##temp_data["Cri3"] = data_frame.apply(lambda x: identify_phrase(x.Call,each_key, False), axis=1)
            ##temp_data["Cri4"] = data_frame.apply(lambda x: identify_phrase(x.Call,each_key, True), axis=1)
            temp_data["File"] = each_csv
            temp_data = temp_data.loc[(temp_data["Cri1"]==True)]
            ###| (temp_data["Cri2"]==True) | (temp_data["Cri3"]==True) | (temp_data["Cri4"]==True)]
            total_data = pd.concat([total_data, temp_data], axis=0)

# %%
#### target_dir is the corresponding group folder in the output folder, which is also passed in the submit script ###
    os.chdir(target_dir_group)
    #### save a information file ###
    total_data.to_csv("FR5.csv", index=None)
