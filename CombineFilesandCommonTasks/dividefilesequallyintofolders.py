import argparse
import os
import shutil

N = 240  # the number of files in seach subfolder folder

dir = r"C:\Users\jasonjia\Dropbox\ConferenceCall\Output\KeywordIdentification\Filled Set of 50 Group Folders"

def move_files(dir):
    """Move files into subdirectories."""

    files = [os.path.join(dir, f) for f in os.listdir(dir) if '.csv' in f]

    i = 0
    j = 0
    curr_subdir = None

    for f in files:
        # create new subdir if necessary
        if i % N == 0:
            j = j + 1
            subdir_name = os.path.join(dir, "group" + str(j))
            curr_subdir = subdir_name

        # move file to current dir
        f_base = os.path.basename(f)
        shutil.move(f, os.path.join(subdir_name, f_base))
        i += 1


move_files(os.path.abspath(dir))

