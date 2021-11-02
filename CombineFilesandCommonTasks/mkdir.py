from pathlib import Path
import os

cd = Path(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\Empty Set of 50 Group Folders")
os.chdir(r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\Empty Set of 50 Group Folders")

numberofgroups = 50
for i in range(1, numberofgroups + 1):
    os.mkdir("group" + str(i))  