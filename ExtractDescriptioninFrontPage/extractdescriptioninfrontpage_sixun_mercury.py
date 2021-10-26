import pandas as pd
from pathlib import Path
import re
homepath = str(Path.home())
print("The home path detected is {}.".format(homepath))

if r"C:\Users\jasonjia" in homepath:
    windows = True
    print("Detected Windows home path - using Jason's Dropbox folders")
    txtfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txt") 
    #C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txt
    #C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txtandeditedxls\batch1
    outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall")
    xlshtmlfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Xls")
    #C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txtandeditedxls\batch1
    #C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Xls
    
else:
    windows = False
    print("Assuming Mercury home path - using Mercury folders")
    txtfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/RawScripts")
    outputfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription")
    xlshtmlfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/List")


colname = "Frontpagedescription"
outputsuffix = "_withfrontpagedesc"
txtpath = Path(txtfolder)
# table = pd.DataFrame()

startkeywordlist1 = ['EDITED TRANSCRIPT', 'EDITED BRIEF', 'PRELIMINARY TRANSCRIPT', 
                    'FINAL TRANSCRIPT', 'PRELIMINARY BRIEF', 'Transcript produced and provided by']
startkeywordlist2 = ['Fair Disclosure Financial Network, Inc. For more information: www.fdfn.com',
                    '1-617-393-3354', 'These reports were compiled using a product of Thomson Reuters',
                    'affiliated companies.']

# pagenumberregex = re.compile("[0-9]{1,4}\n")
# x = pagenumberregex.fullmatch("221\n")
endkeywordlist = ['EVENT DATE/TIME', 'Event Date/Time']

def findlinenumber(contents, quote):
    for linenumber, line in enumerate(contents):
        if quote in line:
            print(linenumber)

def nearby(contents, linenumber, area=20):
    print(contents[linenumber-area:linenumber+area+1])
    
def getstartlist_endlist(contents):
    startlist = []
    endlist = []
    count = 0
    
    for linenumber, line in enumerate(contents): 
        endcond1 = any(endkeyword in line for endkeyword in endkeywordlist)
        endcond2 = 'Disclaimer: The information contained herein is the Fair Disclosure Financial Network' in line and contents[linenumber - 1] == '\n' and contents[linenumber - 2]!= '\n'
        endcond3 = line.strip().lower() == 'event transcript' and contents[linenumber + 1].strip() != 'TRANSCRIPT PRODUCED BY FAIR DISCLOSURE FINANCIAL NETWORK, INC.'
        if endcond1 or endcond2 or endcond3:
            # print(linenumber, line)    
            endlist.append(linenumber)
    
    for linenumber, line in enumerate(contents):            
        if len(startlist) == len(endlist):
            break
        startcond1a = any(startkeyword in line for startkeyword in startkeywordlist1)
        startcond2a = any(startkeyword in line for startkeyword in startkeywordlist2)
        startcond1b = endlist[count] - linenumber < 20
        startcond1c = endlist[count] > linenumber
        if (startcond1a or startcond2a) and startcond1b and startcond1c:
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
        # print(string)
        list.append(string)
    
    return list

errorpd = pd.DataFrame()

for txtfile in txtfolder.iterdir():
    filestem = txtfile.stem
    outputfile = filestem + outputsuffix + '.xlsx'
    outputpath = Path(outputfolder / outputfile)
    
    if outputpath.exists() == False and txtfile.suffix == '.txt':
        
        file = open(txtfile, 'r', errors='ignore')
        contents = file.readlines()
        startlist, endlist = getstartlist_endlist(contents)
        list = getlistofdescriptions(startlist, endlist)
        
        xlshtmlfile = filestem + '.xls'
        xlshtmlpath = Path(xlshtmlfolder / xlshtmlfile)    
        try:
            xlshtml = pd.read_html(xlshtmlpath)[0]
        except ValueError:
            xlshtml = pd.read_excel(xlshtmlpath)
        
        xlshtml_numberofrows = xlshtml.shape[0]
        list_numberofrows = len(list)
        if xlshtml_numberofrows != list_numberofrows:
            print("Error: shape of df ({}) =/= shape of list in {} ({})".format(xlshtml_numberofrows, xlshtmlfile, list_numberofrows))
            errorpd = errorpd.append(pd.Series(xlshtmlfile), ignore_index=True)
            if windows:
                #break
                1
        elif xlshtml_numberofrows == 0:
            print("Both df and list in {} have 0 entries.".format(xlshtmlfile))
        else:
            xlshtml[colname] = pd.DataFrame(list)

            writer = pd.ExcelWriter(outputpath)
            xlshtml.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            writer.close()
            print("Generated front page desciption for: " + str(txtfile))
for i in errorpd:
    print(i)        
# want to know how many reports there are per file - import xls, read number of entries

# get the page numbers 
# C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\Txt






