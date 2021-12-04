#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
import pandas as pd

def import_proj_dir():
    homepath = str(Path.home())
    print("Home path: {}".format(homepath))
    
    if r"C:\Users" in homepath: 
        print("Importing proj_dir_windows.csv")
        proj_dir = pd.read_csv(r"C:\Users\jasonjia\Dropbox\Projects\conference_call\code\00_create_proj_dir\proj_dir_windows.csv", header=None, index_col=0, squeeze=True).to_dict()
    else:
        print("Importing proj_dir_mercury.csv")
        proj_dir = pd.read_csv(r"C:\Users\jasonjia\Dropbox\Projects\conference_call\code\00_create_proj_dir\proj_dir_mercury.csv", header=None, index_col=0, squeeze=True).to_dict()
        
    return proj_dir

def get_folder(root, suffix):
    proj_dir = import_proj_dir()
    key = root + '_' + suffix
    if not(key in proj_dir.keys()):
        print("Key '{}' does not exist in proj_dir. No folder retrieved.".format(key))
        return;
    
    folderpath = Path(proj_dir[key])        
    return folderpath