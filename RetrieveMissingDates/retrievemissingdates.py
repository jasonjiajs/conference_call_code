import pynput
import time
from pynput import mouse as MS
from pynput import keyboard as KB
from pynput.keyboard import Key
from datetime import datetime
import pyperclip
import os
import numpy as np
import io
import pandas as pd

# Overall structure:
# 1. load the excel file and get the report numbers
# 2. parse into 25-bit pieces
# 3. enter search into thomson reuters, download the xls file, get the dates
# 4. compile the dates
# 5. copy back the dates into the excel file.

# 1. load the excel file and get the report numbers

inputfolder = "C:\\Users\\jasonjia\\Dropbox\\ConferenceCall\\Output\\RetrieveMissingDates"
inputfile = "paragraph_datemissing.xlsx"

df = pd.read_excel(inputfolder + "\\" + inputfile)

reportid = pd.DataFrame(df['report'])

# 2. parse into 25-bit pieces

maxnumberofsearches = 25
q, _ = divmod(np.arange(len(reportid)), maxnumberofsearches)
groups = list(reportid.groupby(q))
searchterms = []
numberofsearchterms = max(q) + 1
 
for i in range(numberofsearchterms):
    chunk = groups[i][1]
    chunk = chunk.to_csv(header=False, index=False).strip('\n').split('\n')
    chunk = '; '.join(chunk).replace('\r','').replace('\n','')
    searchterms += [chunk]
# 3. enter search into thomson reuters, download the xls file, get the dates

#---------------------------- Functions -------------------------------------#

#### open keyboard and mouse Controller ####
KB_enter = pynput.keyboard.Controller()
MS_enter = pynput.mouse.Controller()

##### click mouse function ####
def mouse_click(position,delay=0):
    MS_enter.position = position
    MS_enter.click(pynput.mouse.Button.left,1)
    if delay>0:
        time.sleep(delay)
##### type string function ###
def key_strtype(e_string):
    KB_enter.type(e_string)
##### press key function ####
def key_press(key):
    KB_enter.press(key)
    KB_enter.release(key)
##### generate ideal file name #####
def file_name(directory, name):
    return directory + '\\' + name
##### check if file is downloaded ####
def existing_file(directory, name, exten_name):
    full_name = name + exten_name
    if full_name in os.listdir(directory):
        return True
    else:
        return False
    
mouse_c_adj = (0,-20)
mouse_c_list_2_initial = [(32, 852), [(1678, 788),(1712, 788)], (1315, 1019), (1348, 992), (56, 819), (557, 321), (554, 764), (32, 852), (1854, 786)]
mouse_c_list_2 = [(32+mouse_c_adj[0], 852+mouse_c_adj[1]), 
                  [(1678+mouse_c_adj[0]-382, 788+mouse_c_adj[1]),
                   (1712+mouse_c_adj[0]-382, 788+mouse_c_adj[1])], 
                  (1315+mouse_c_adj[0]-185, 1019+mouse_c_adj[1]-165),
                  (1348+mouse_c_adj[0]-185, 992+mouse_c_adj[1]-155), 
                  (56+mouse_c_adj[0], 819+mouse_c_adj[1]), 
                  (557+mouse_c_adj[0]-190, 321+mouse_c_adj[1]-70), 
                  (554+mouse_c_adj[0]-190, 764+mouse_c_adj[1]-70), 
                  (32+mouse_c_adj[0], 852+mouse_c_adj[1]), 
                  (1854+mouse_c_adj[0]-380, 786+mouse_c_adj[1])]


#%%
time.sleep(1)
mouse_click((302+mouse_c_adj[0],120+mouse_c_adj[1]),2) ### research

# Where you'll be saving your excel files
outputfolder = "C:\\Users\\jasonjia\\Dropbox\\ConferenceCall\\Output\\RetrieveMissingDates"

for i in range(numberofsearchterms):
    outputfile = 'chunk_' + str(i) 
# Type in contributor - Refinitiv Streetevents
    if not existing_file(outputfolder, outputfile, ".xls"):
        time.sleep(1)
        mouse_click((90,510),0.5) ### contributor
        with KB_enter.pressed(Key.ctrl):
            key_press('a')
        key_strtype(searchterms[i])
        time.sleep(1.5)
        
        #### search ####
        key_press(Key.enter) ### search results displayed for the time period
        #### wait for the results to display ####
        time.sleep(2)
        
        ### select all reports
        mouse_click(mouse_c_list_2[0], 1)
        # click on the excel button
        mouse_click(mouse_c_list_2[1][1],1)
        time.sleep(1)
        ## ii. Select save and save as
        mouse_click(mouse_c_list_2[2],1)
        mouse_click(mouse_c_list_2[3],1)
        
        ## iii. Enter the name of the excel and save it
        key_strtype(outputfolder + "\\" + outputfile)
        time.sleep(0.5)
        key_press(Key.enter)
        time.sleep(1)
        
#%%
# The "excel" file looks like a .xls file, but it's actually a html file readable with excel.
# What a terrible thing for Thomson One to pull off...

table = pd.DataFrame()

os.chdir(outputfolder)
for i in range(numberofsearchterms): #for file_i in os.listdir(outputfolder):
    file_i = 'chunk_' + str(i) + '.xls'
    print(file_i)
    chunktable = pd.read_html(file_i)[0]
    chunktable = chunktable[['Date','Report #']]
    table = table.append(chunktable)

matchingtable = reportid.merge(table, how='inner', left_on='report', right_on='Report #')
matchingtable = matchingtable.drop_duplicates()
matchingtable = matchingtable.drop('Report #',axis=1)
print('The original excel file with missing dates has {a} missing entries. '\
      'Removing duplicates, there are missing dates for {b} unique reports. '\
      'After downloading the reports, consolidating the "xls" files and ' \
      'merging the dates with only the report IDs from the original excel ' \
      'file, we found {c} unique dates. Check that {b} == {c}.'\
      .format(a=len(reportid), b=len(reportid.drop_duplicates()), c=len(matchingtable)))

# finaltable['Date'].dtypes # 'O' = string (I think)
matchingtable['Date'] = pd.to_datetime(matchingtable['Date'], infer_datetime_format = True)
matchingtable['Date'] = matchingtable['Date'].dt.strftime('%Y-%m-%d')

finaltable = reportid.merge(matchingtable, how='left', on='report')

writer = pd.ExcelWriter(inputfolder + "\\" + 'output.xlsx')
finaltable.to_excel(writer, 'finaltable')
writer.save()


