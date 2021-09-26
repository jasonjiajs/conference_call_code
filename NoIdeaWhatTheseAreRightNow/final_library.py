###### Created by SIXUN TANG @20200316
###### This python file serves to generate bigrams in the political libraries but not in non-political libraries
###### Raw input is the political as well as non-political bigrams from previous codes

### create political bigrams list, with weight
with open("political_bigrams.txt","r",encoding="utf-8", errors="ignore") as p_lib:
    p_lib_text = p_lib.readlines()
    p_lib_list = []
    total_length = len(p_lib_text)-1
    for item in p_lib_text[1:]:
        item_list = item.split("\t")
        word = item_list[0]
        appearance = item_list[1]
        weight = int(appearance)/total_length * 100000
        p_lib_list.append((word,weight))

#### create non-political bigrams list and weight
with open("non_political_bigrams_1.txt","r",encoding="utf-8", errors="ignore") as np_lib:
    np_lib_text = np_lib.readlines()
    np_lib_list = []
    total_length = len(np_lib_text)-1
    for item in np_lib_text[1:]:
        item_list = item.split("\t")
        word = item_list[0]
        appearance = item_list[1]
        weight = int(appearance)/total_length * 100000
        np_lib_list.append((word,weight))

with open("non_political_bigrams_2.txt","r",encoding="utf-8", errors="ignore") as np_lib2:
    np_lib2_text = np_lib2.readlines()
    total_length = len(np_lib2_text)-1
    for item in np_lib2_text[1:]:
        item_list = item.split("\t")
        word = item_list[0]
        appearance = item_list[1]
        weight = int(appearance)/total_length * 100000
        np_lib_list.append((word,weight))

### define functions for generating A\B library
### could be used in the future to generate NP\P library
def diff_gen(list1, list2, file_name):
    list1 = sorted(list1, key = lambda item: item[1], reverse= True)
    exclude_list = [item[0] for item in list2]
    with open(file_name,"w",encoding="utf-8", errors="ignore") as o_file:
        print("Bigrams\tWeight", file=o_file)
        for word_item in list1:
            if word_item[0] not in exclude_list:
                print("%s\t%.2f"%(word_item[0],word_item[1]), file=o_file)

#### generate political but not non-political libraries ###
diff_gen(p_lib_list,np_lib_list,"p_not_np_lib.txt")