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

inputfolder = "C:\\Users\\jasonjia\\Dropbox\\ConferenceCall\\Output\\KeywordIdentification\entry_files_combined\\sixunandjason\\v3"
inputfile = "reportswithmissingtitles.xlsx"

df = pd.read_excel(inputfolder + "\\" + inputfile, header=None)


# 2. parse into 25-bit pieces

maxnumberofsearches = 25
q, _ = divmod(np.arange(len(df)), maxnumberofsearches)
groups = list(df.groupby(q))
searchterms = []
numberofsearchterms = max(q) + 1
 
for i in range(numberofsearchterms):
    chunk = groups[i][1]
    chunk = chunk.to_csv(header=False, index=False).strip('\n').split('\n')
    chunk = '; '.join(chunk).replace('\r','').replace('\n','')
    searchterms += [chunk]
    print(chunk)
    print("\n")