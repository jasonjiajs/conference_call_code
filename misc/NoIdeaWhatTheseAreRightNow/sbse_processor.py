###### Created by SIXUN TANG @20200320
###### This python file serves to generate spokne english bigrams from SBSE(parsed from trn, raw input are in text files)
###### And add restrictions based on Hassan et al.


### packages ###
from nltk import bigrams
from nltk import word_tokenize
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords 
from nltk import FreqDist
from nltk import PerceptronTagger
import string

### Function I: get rid of weird symbol and punctuation ####
def punc_reader(text, punc = False):
    new_text = ""
    for posi in range(len(text)):
        char = text[posi]
        if not char.isalpha() and not char.isalnum() and char!=" ":
            if punc==False:
                if char in string.punctuation:
                    pass
            else:
                if char == "-":
                    char = " "
                else:
                    continue
        new_text += char
    return ' '.join(new_text.split())

#### Function II: Define bigrams that should be deleted ####
#### For Perceptron, the list of word properties could be found in https://cs.nyu.edu/grishman/jet/guide/PennPOS.html
def del_bigrams(tuple):
    prop1 = tuple[0][1]
    word1 = tuple[0][0].lower()
    prop2 = tuple[1][1]
    word2 = tuple[1][0].lower()
    word_del = ['i','ive','youve','weve','im','youre','were','id','youd','wed','thats']
    adverb = ['RB','RBR','RBS','TO']
    pronoun = ['PRP','PRP$']
    whadverb = ['WRB']
    preposition = ['IN']
    determiner = ['DT']
    if prop1 in preposition and prop2 in preposition: #### preposition + preposition ####
        return True
    elif prop1 in pronoun and prop2 in pronoun: ### pronoun+pronoun ###
        return True
    elif prop1 in adverb and prop2 in adverb:
        return True
    elif prop1 in whadverb and prop2 in adverb:
        return True
    elif (prop1 in preposition and prop2 in adverb) or ((prop1 in adverb and prop2 in preposition)):
        return True
    elif (prop1 in preposition and prop2 in whadverb) or ((prop1 in whadverb and prop2 in preposition)):
        return True
    elif (prop1 in preposition and prop2 in determiner) or ((prop1 in determiner and prop2 in preposition)):
        return True
    elif (prop1 in adverb and prop2 in whadverb) or ((prop1 in whadverb and prop2 in adverb)):
        return True
    elif (prop1 in determiner and prop2 in adverb) or ((prop1 in adverb and prop2 in determiner)):
        return True
    elif (prop1 in determiner and prop2 in whadverb) or ((prop1 in whadverb and prop2 in determiner)):
        return True
    elif word1 in word_del or word2 in word_del:
        return True
    elif word1+word2 == "princetonuniversity":
        return True
    #### delete any bigrams that contain numbers ####
    if num_iden(word1) or num_iden(word2):
        return True
    return False

#### Function III: define to see if a string is all numbers ####
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

#### spoken English  ######
p_lib_text = ''
with open("Training Library\\SBSE.txt", "r", encoding="utf-8", errors="ignore") as p_library:
    for line in p_library.readlines():
        p_lib_text += punc_reader(line, True).lower() + "\n"   ### rid of punctuation and lowercase

p_lib_list_raw = word_tokenize(p_lib_text)
#### link the hyphenate across lines ####
p_lib_list = []
word_next = ''
for posi in range(len(p_lib_list_raw)):
    word = p_lib_list_raw[posi]
    if word.endswith("-"):
        word_next = p_lib_list_raw[posi+1]
        p_lib_list.append(word+word_next)
        continue
    if word==word_next:
        continue
    p_lib_list.append(word)
    word_next = ''

#### add tagger #### 
tagger = PerceptronTagger()

tagger_list = tagger.tag(p_lib_list)

bigrams_list_raw = list(bigrams(tagger_list))


### delete bigrams of certain property using function ####
bigrams_list = []
for bigram_item in bigrams_list_raw:
    if not del_bigrams(bigram_item):
        word1 = bigram_item[0][0]
        word2 = bigram_item[1][0]
        if word1+' '+word2 !="confirming pages":
            bigrams_list.append((word1,word2))



#### generate bigram frequency list ####
bigram_dict = FreqDist(bigrams_list)
bigram_rank = sorted(dict(bigram_dict).items(), key = lambda item: item[1], reverse=True)

### save the bigram list ####
total_length = len(bigram_rank)
print(total_length)
### print to bigram text file, with weight(*100000) ####
with open("non_political_bigrams_2.txt","w",encoding="utf-8",errors="ignore") as p_file:
    print("Bigrams\tTime\tFrequency", file=p_file)
    for items in bigram_rank:
        print("%s\t%d\t%.2f"%(items[0][0]+" "+items[0][1], items[1], items[1]/total_length*100000), file=p_file)



