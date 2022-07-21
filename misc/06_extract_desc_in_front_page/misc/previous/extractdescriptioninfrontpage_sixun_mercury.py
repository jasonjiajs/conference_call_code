import pandas as pd
from pathlib import Path

txtfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/RawScripts")
outputfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription")
xlshtmlfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/List")
 
colname = "Frontpagedescription"
outputsuffix = "_withfrontpagedesc"
txtpath = Path(txtfolder)
# table = pd.DataFrame()

def getlistofdescriptions(contents):
    startlist = []
    endlist = []
    
    for linenumber, line in enumerate(contents):
        if ("EDITED TRANSCRIPT" in line) or ("EDITED BRIEF" in line):
            # print(linenumber, line)
            startlist.append(linenumber)
        if "EVENT DATE/TIME:" in line:
            # print(linenumber, line)    
            endlist.append(linenumber)
            
    list = []
    
    for entrynumber, startlinenumber in enumerate(startlist):
        endlinenumber = endlist[entrynumber]
        # print(startlinenumber, endlinenumber)
        string = ""
        for i in range(startlinenumber+1, endlinenumber):
            string = string + " " + contents[i].strip()
        # print(string)
        list.append(string)
    
    return list


for txtfile in txtfolder.iterdir():
    if txtfile.suffix == '.txt':
        print(txtfile)
        file = open(txtfile, 'r', errors='ignore')
        contents = file.readlines()
        list = getlistofdescriptions(contents)
        
        filestem = txtfile.stem
        
        xlshtmlfile = filestem + '.xls'
        xlshtmlpath = Path(xlshtmlfolder / xlshtmlfile)    
        xlshtml = pd.read_html(xlshtmlpath)[0]
        xlshtml[colname] = pd.DataFrame(list)
        
        outputfile = filestem + outputsuffix + '.xlsx'
        outputpath = Path(outputfolder / outputfile)
        writer = pd.ExcelWriter(outputpath)
        xlshtml.to_excel(writer, 'Sheet1', index=False)
        writer.save()
        writer.close()
        
# want to know how many reports there are per file - import xls, read number of entries

# get the page numbers 
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txt








