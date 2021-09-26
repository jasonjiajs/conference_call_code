from nltk import bigrams
from nltk import word_tokenize
from nltk import FreqDist
from nltk import PerceptronTagger
import re
import sys
import string
import datetime

##### By: Sixun Tang @20200315
##### Add New Part @20200319
##### This python code serves to generate the political risk index in Hassan et al. for single firm from conference call scripts
#####  Input: bigram dictionary constructed ahead of time; Syonyms dictionary; Raw call scripts
#####  Function: i. Delete Character Names ii. Delete Numbers and Punctuations; iii. Other restrictions in Hassan

script_raw = sys.argv[1]
csv_date = sys.argv[2]

csv_date_date = datetime.date(year=int(csv_date[:4]), month = int(csv_date[4:6]), day = int(csv_date[6:8]))




call_script = ''

#### initial deal with the call script ####
#### delete speaker names and information ####
#### split different speakers by \n ####

##### get rid of strange symbols and punctuations #####
def bigram_initial(text,punct=False): ### if punct = True, get rid of all punctuations. This function serves to generate the input for nltk bigrams
    text_list = word_tokenize(text)
    nopunct_list = []
    if punct == True: ### get rid of all punctuation
        for w_item in text_list:
            for char in w_item:
                if char.isalpha() or char in '0123456789':
                    nopunct_list.append(w_item)
                    break
        text_list = nopunct_list
    return text_list

def risk_count(text, word_set, bigram): ### raw input is the text list, the synonym set and the bigram position
    low_bound = bigram[0]-9
    up_bound = bigram[1]+9
    risk_list = []
    for item in text[low_bound:up_bound]:
        if item in word_set:
            risk_list.append(item)
    if risk_list==[]:
        return 0, risk_list
    else:
        return 1, risk_list 

## this function helps us to identify character line###
def identify_character_line(char_line):
    line_list = char_line.replace("\n","").split()
    title_word = 0
    count_word = 0
    for word in line_list:
        if word in string.punctuation or word == "--":
            if word=="-":
                pass
            else:
                continue
        else:
            count_word += 1
        if word.islower() and line_list.index(word)==0: ### if the first word is not capitalized
            return False
        if not word.islower() and word!="-": #### if a word is not "-", and is not lowercase for all letters, count it as a title word
            title_word += 1 
        if word == "-": ### "-" is a symbol that only contained in character line(as a separate one), and always there is a name before this symbol
            if title_word==count_word:
                return True
        if line_list.index(word)==len(line_list)-1: ### to the last position and nothing reached
            if title_word/count_word>=0.8: ### more than 80% words are not lower case
                return True
            else:
                return False

#### function to see if a string is all numbers ####
def num_iden(string):
    total_length = len(string)
    num_length = 0
    for char in string:
        if char in '0123456789':
            num_length +=1
    if total_length==num_length:
        return True
    else:
        return False

with open(script_raw, "r", encoding="utf-8", errors="ignore") as call_text:
    paragraph_list = []
    para_str = ''
    for line in call_text.readlines():
        if identify_character_line(line):  ### if character line, ignore it
            continue
        elif line == "\n":
            if para_str!='':
                paragraph_list.append(para_str)
            para_str = ''
        else:
            ### additional modification i. replace specific words ####
            line_result = line.replace("Bill","bbill")
            line_result = line_result.replace("Constitution","cconstitution")
            para_str += line.replace("\n"," ").lower()


### additional restrictions borrowed from Hassan ###
    safe_harbor = ['safe', 'harbor', 'forwardlooking', 'forward', 'looking', 'actual', 'statements', 'statement', 'risk', 'risks', 'uncertainty', 'uncertainties', 'future', 'events', 'sec',\
'results']
    risk_synonyms = ["risk officer", "risk credit officer", "unknown speaker", "unknown participant", "unknown speaker", "unknown participant", "unknown caller", "unknown operator", "unknown firm analyst", "in the states"]
#### i. remove snippets ####
#### for year before 2005q1, we could not identify small paragraphs, so we just do not do this step.
for i in range(len(paragraph_list)):
    para_item = paragraph_list[i]
    safe_harbor_num = 0
    if csv_date_date>=datetime.date(year=2005, month=4, day=1): #### after 2005q1, we remove snippets
        if 'forwardlooking' in bigram_initial(para_item,True) and i<len(paragraph_list)/2:
            continue
        for word_item in safe_harbor:
            if word_item in bigram_initial(para_item,True):
                safe_harbor_num += 1
            if safe_harbor_num>2:
                continue
        if safe_harbor_num>2 and i<len(paragraph_list)/2:  ### first half of the script with more than 2 safe harbor words
            continue
    if call_script == '':
        call_script += para_item
    else:
        call_script += ' '+para_item

#### ii. remove bigrams which contain pronouns, short pronouns or two adverbs(tagger first) #####
call_word_list_raw = bigram_initial(call_script, True)

#### add tagger #### 
tagger = PerceptronTagger()

tagger_list_raw = tagger.tag(call_word_list_raw)

tagger_list = []
no_append = False
for i in range(len(tagger_list_raw)):
    two_word_combo1 = ""
    two_word_combo2 = ""
    three_word_combo1 = ""
    three_word_combo2 = ""
    if i<= len(tagger_list)-2:
        two_word_combo1 = tagger_list_raw[i][0] + tagger_list_raw[i+1][0]
    if i<= len(tagger_list)-3:
        three_word_combo1 = tagger_list_raw[i][0] + tagger_list_raw[i+1][0] + tagger_list_raw[i+2][0]
    if i>= 1:
        two_word_combo1 = tagger_list_raw[i][0] + tagger_list_raw[i-1][0]
    if i>= 2:
        three_word_combo2 = tagger_list_raw[i][0] + tagger_list_raw[i-1][0] + tagger_list_raw[i-2][0]
    if two_word_combo1 in risk_synonyms or two_word_combo2 in risk_synonyms or three_word_combo1 in risk_synonyms or three_word_combo2 in risk_synonyms:
        continue
    tagger_list.append(tagger_list_raw[i])

call_word_list = []
for i in range(len(tagger_list)):
    call_word_list.append(tagger_list[i][0])


call_bigram_list_raw = list(bigrams(tagger_list))

### delete bigrams of ii and contain numbers####
def bigram_filter(tuple):
    prop1 = tuple[0][1]
    word1 = tuple[0][0].lower()
    prop2 = tuple[1][1]
    word2 = tuple[1][0].lower()
    ### additional words and phrases that need to be removed ####
    adverb = ['RB','RBR','RBS','TO','WRB']
    pronoun = ['PRP','PRP$']
    if prop1 in adverb and prop2 in adverb: ###two adverbs
        return True
    elif prop1 in pronoun or prop2 in pronoun: ### bigrams which contain pronouns
        return True
    #### delete any bigrams that contain numbers ####
    if num_iden(word1) or num_iden(word2):
        return True
    return False

call_bigram_list = []
call_list_posi = []
for i in range(len(call_bigram_list_raw)):
    bigram_item = call_bigram_list_raw[i]
    if not bigram_filter(bigram_item):
        word1 = bigram_item[0][0]
        word2 = bigram_item[1][0]
        call_bigram_list.append((word1,word2))
        call_list_posi.append(i)



### open bigrams dictionary ####
### And create a dictionary and list for the top 120 bigrams ###
top_120 = []
top_dict = {}
with open("p_not_np_lib.txt","r",encoding="utf-8", errors="ignore") as np_set:
    p_lib_dict = {}
    p_lib = np_set.readlines()
    count_bi = 0
    for item in p_lib[1:]:
        count_bi += 1
        key, value = item.split("\t")[0], float(item.split("\t")[1])
        p_lib_dict[key] = value
        if count_bi<=120:
            top_120.append(key)
            top_dict[key] = 0
    

### open synonyms ###
with open("synonym.txt","r",encoding="utf-8", errors="ignore") as synonym:
    synonyms = []
    char_syn = ''
    for char in synonym.readline():
        if char.isalpha():
            char_syn += char
        else:
            if char_syn!="":
                synonyms.append(char_syn)
                char_syn = ''

### risk measure ###
risk_measure = 0
o_risk = 0 
for i in range(len(call_bigram_list)):
    words = call_bigram_list[i][0]+" "+ call_bigram_list[i][1]
    if call_bigram_list[i][0] in synonyms or call_bigram_list[i][1] in synonyms :
        o_risk += 10000/len(call_bigram_list)
    r_measure,ris_syn = risk_count(call_word_list, synonyms,(call_list_posi[i],call_list_posi[i]+1))
    if words not in p_lib_dict.keys():
        continue
    elif r_measure==0:
        continue
    else:
        risk_measure += 10000*p_lib_dict[words]/len(call_bigram_list)  ### in counting length, we take the numbers into account ### 
        if words in top_dict.keys():
            top_dict[words] = top_dict[words] + 1


print("%.4f"%(risk_measure))
print("%.4f"%(o_risk))
for i in range(120):
    top_b = top_120[i]
    print("%d"%(top_dict[top_b]))