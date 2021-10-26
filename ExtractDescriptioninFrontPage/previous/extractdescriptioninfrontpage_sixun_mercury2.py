import pandas as pd
from pathlib import Path

txtfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/RawScripts")
outputfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription")
xlshtmlfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/List")
 
colname = "Frontpagedescription"
outputsuffix = "_withfrontpagedesc"
txtpath = Path(txtfolder)
# table = pd.DataFrame()

startkeywordlist = ['EDITED TRANSCRIPT', 'EDITED BRIEF', 'PRELIMINARY TRANSCRIPT', 'FINAL TRANSCRIPT']
endkeywordlist = ['EVENT DATE/TIME', 'Event Date/Time']

def getstartlist_endlist(contents):
    startlist = []
    endlist = []
    count = 0
    
    for linenumber, line in enumerate(contents):
        if any(endkeyword in line for endkeyword in endkeywordlist):
            # print(linenumber, line)    
            endlist.append(linenumber)
    
    for linenumber, line in enumerate(contents):            
        if len(startlist) == len(endlist):
            break
        if any(startkeyword in line for startkeyword in startkeywordlist) and abs(endlist[count] - linenumber) < 5:
            # print(linenumber, line)
            startlist.append(linenumber)
            count = count + 1

    return startlist, endlist

def getlistofdescriptions(startlist, endlist):
            
    list = []
    
    for entrynumber, startlinenumber in enumerate(startlist):
        endlinenumber = endlist[entrynumber]
        # print(startlinenumber, endlinenumber)
        
        string = ""
        for i in range(startlinenumber+1, endlinenumber):
            string = string + " " + contents[i].strip()
        print(string)
        list.append(string)
    
    return list

errorpd = pd.DataFrame()

for txtfile in txtfolder.iterdir():
    if txtfile.suffix == '.txt':
        print(txtfile)
        file = open(txtfile, 'r', errors='ignore')
        contents = file.readlines()
        startlist, endlist = getstartlist_endlist(contents)
        list = getlistofdescriptions(startlist, endlist)
        
        filestem = txtfile.stem
        
        xlshtmlfile = filestem + '.xls'
        xlshtmlpath = Path(xlshtmlfolder / xlshtmlfile)    
        xlshtml = pd.read_html(xlshtmlpath)[0]
        
        if xlshtml.shape[0] != len(list):
            print("Error: shape of df =/= shape of list in {}".format(xlshtmlfile))
            errorpd = errorpd.append(pd.Series(xlshtmlfile), ignore_index=True)
        else:
            xlshtml[colname] = pd.DataFrame(list)
            
            outputfile = filestem + outputsuffix + '.xlsx'
            outputpath = Path(outputfolder / outputfile)
            writer = pd.ExcelWriter(outputpath)
            xlshtml.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            writer.close()

for i in errorpd:
    print(i)        


# want to know how many reports there are per file - import xls, read number of entries

# get the page numbers 
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txt








