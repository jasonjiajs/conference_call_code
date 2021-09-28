### this code serves to bold the keywords ### 

#%%%
import openpyxl
import xlsxwriter
import re

#%% This wasn't in the original code...
os.chdir("C:/Users/jasonjia/Dropbox/ConferenceCall/Output/KeywordIdentification")

#%%%
raw_data = openpyxl.load_workbook(r"cric1_newtotal.xlsx")[raw_data.sheetnames[0]] # choose first sheet of the workbook 
# (there's only one sheet but we want a sheet object)

#%%
row = 0 
col = 0
with open("keyterms.txt", "r", encoding="utf-8", errors="ignore") as f1:
    key_set = set(f1.read().splitlines())
keyw_list = list(key_set) 
keyw_list = [t.lower() for t in keyw_list]


#%%% title
title_file = openpyxl.load_workbook(r"Entry mask.xlsx")[title_file.sheetnames[0]]

#%%% overview
overview_file = xlsxwriter.Workbook("Paragraph Record.xlsx")
w1 = overview_file.add_worksheet()
w1.write(0,0,"File Name")
w1.write(0,1,"Starting Row")
w1.write(0,2,"Ending Row")
w1.write(0,3,"Name of RA")

dict_title = {0:2, 2:6, 3:7, 4:8, 5:9, 7:44, 15:45}

for row_val in range(1,raw_data.max_row):
    if row_val%500==1:
        if row_val//500>0:
            final_data.close()
        final_data = xlsxwriter.Workbook(r"entry_files/"+ str(row_val//500+1) + ".xlsx")
        bold_1 = final_data.add_format({"bold":True}) # the bold "format"
        worksheet = final_data.add_worksheet()
        w1.write(row_val//500+1,0,row_val//500+1)
        w1.write(row_val//500+1,1,row_val)
        if row_val//500 + 1>1:
            w1.write(row_val//500,2,row_val-1)//7
        #%%% write title 
        for row_val_1 in range(2):
            for col_val_1 in range(title_file.max_column):
                worksheet.write(row_val_1,col_val_1,title_file.cell(row_val_1+1,col_val_1+1).value,bold_1) # bolding of titles - not that important
    keyw = raw_data.cell(row_val+1,0+1).value
    text = raw_data.cell(row_val+1,1+1).value
    in_list_key = []
    for i in keyw_list:
        if i in text.lower():
            in_list_key.append(i)
    new_text = re.split("|".join(in_list_key),text,flags=re.I)
    format_text = []
    for i in range(len(new_text)):
        splited_text = new_text[i]
        if splited_text!="":
            format_text.append(splited_text)
        if i<len(new_text)-1:
            format_text.append(bold_1)
            for each_key in in_list_key:
                test_text = splited_text + each_key
                if test_text.lower() in text.lower():
                    format_text.append(each_key)
                    break
    for col_val in dict_title.keys():
        worksheet.write((row_val-1)%500+2, dict_title[col_val],raw_data.cell(row_val+1,col_val+1).value)

    worksheet.write_rich_string((row_val-1)%500+2,5,*format_text)
    worksheet.write((row_val-1)%500+2, 1, row_val)
    if row_val == raw_data.max_row-1:
        w1.write(row_val//500+1,2,row_val)
        final_data.close()


overview_file.close()
# %%
