from pathlib import Path
import pandas as pd
import shutil

homepath = str(Path.home())
print("The home path detected is {}.".format(homepath))

if r"C:\Users\jasonjia" in homepath:
    windows = True
    print("Detected Windows home path - using Jason's Dropbox folders")
    pd = pd.read_excel(r'C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall\fileswithmismatchingsizes.xlsx', header=None)
    xlsfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall")
    txtfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall")
    outputfolder = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\ConferenceCall")
    
else:
    windows = False
    print("Assuming Mercury home path - using Mercury folders")
    pd = pd.read_excel(r'/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription/fileswithmismatchingsizes.xlsx', header=None)
    xlsfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/List")
    txtfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/RawScripts")
    pdffolder = txtfolder
    outputfolder = Path(r"/project/kh_mercury_1/ConferenceCallData/ListwithFrontPageDescription")


list = pd[0].values.tolist()
for i in list:
    print(i)
    xlsfilename = str(i) + '.xls'
    xlspath = Path(xlsfolder / xlsfilename)
    destination = Path(outputfolder/ xlsfilename)
    shutil.copy(xlspath,destination)

    txtfilename = str(i) + '.txt'
    txtpath = Path(txtfolder / txtfilename)
    destination = Path(outputfolder/ txtfilename)
    shutil.copy(txtpath,destination)

    pdffilename = str(i) + '.pdf'
    pdfpath = Path(pdffolder / pdffilename)
    destination = Path(outputfolder/ pdffilename)
    shutil.copy(pdfpath,destination)
