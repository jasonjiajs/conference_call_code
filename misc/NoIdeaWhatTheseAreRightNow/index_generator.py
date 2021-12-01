import os
import sys
import csv
import time

csv_dir , index_name, order_group = sys.argv[1], sys.argv[2], sys.argv[3]
csv_list = os.listdir(csv_dir)


index_output = open(index_name,"w",encoding="utf-8", errors="ignore")
print("PPV\tTOC\tTitle\tSubtitle\tDate\tPages\tPrice\tContributor\tAnalyst\tLanguage\tReport\tCollection\tPoliticalRisk\tRisk", file=index_output)

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

#### useful function of dealing with one observation of a correct csv####
def column_converter(row_list, csv_name):
    try:
        basic_info = row_list[:12]
        script = row_list[12]
        raw_file_text = "temp" + order_group + ".txt"
        with open(raw_file_text,"w",encoding="utf-8",errors="ignore") as temp_file:
            print(script,file=temp_file)
        return basic_info
    except IndexError:
        print("%s is a problematic csv"%(csv_name))
progress = 0  
top_statistics = [0]*120
for csvs in csv_list:
    csv_date = csvs[:8]
    csv_name = csv_dir + "/" + csvs
        #### now open csv and readlines ####
    with open(csv_name, "r", encoding="utf-8", errors="ignore") as csv_data_base:
        print(csv_name)
        data_base = csv.reader((line.replace('\0','') for line in csv_data_base) )
        row_num = 0
        for row in data_base:
            try:
                row_num += 1
                if row_num==1:
                    continue
                information_firm = column_converter(row, csv_name)
                if information_firm!=None:
                    command_line = "python3 script_index.py temp" + order_group +".txt " + csv_date
                    out = os.popen(command_line)
                    risk_index_raw = out.read()
                    output_data = risk_index_raw.split("\n")
                    risk_index = output_data[0]
                    overall_risk = output_data[1]
                    for i in range(120):
                        top_statistics[i] = top_statistics[i] + int(output_data[i+2])
                    print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(information_firm[0], information_firm[1], information_firm[2],\
                        information_firm[3], information_firm[4], information_firm[5], information_firm[6], information_firm[7], information_firm[8], \
                        information_firm[9], information_firm[10], information_firm[11], risk_index, overall_risk), file=index_output)
                    progress += 1
                    print("%d\t%s"%(progress,information_firm[2]))
                else:
                    break
            except:
                print("Data Error")


#### top bigrams ###
top_120 = []
with open("p_not_np_lib.txt","r",encoding="utf-8", errors="ignore") as np_set:
    p_lib_dict = {}
    p_lib = np_set.readlines()
    count_bi = 0
    for item in p_lib[1:]:
        count_bi += 1
        key, value = item.split("\t")[0], float(item.split("\t")[1])
        if count_bi<=120:
            top_120.append((key, value))
        else:
            break

with open("top_bigrams.txt","w",encoding="utf-8", errors="ignore") as top_b_stats:
    for i in range(120):
        print("%s\t%.2f\t%d"%(top_120[i][0],top_120[i][1], top_statistics[i]), file = top_b_stats)

index_output.close()