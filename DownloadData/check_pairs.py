####################### This file serves to check whether xls and pdf are in pairs ##########
####################### The input is the file_record generated from the automatic_download.py ##############
####################### The output is the missing pdfs or excels ############

import pynput
import time
from pynput import mouse as MS
from pynput import keyboard as KB
from pynput.keyboard import Key
import datetime
from datetime import timedelta
import pyperclip
import os

KB_enter = pynput.keyboard.Controller()
MS_enter = pynput.mouse.Controller()
time.sleep(5)
#### save directory
call_dir = r"C:\Users\stang10\ConferenceCall\CallScripts"
index_dir = r"C:\Users\stang10\ConferenceCall\List"


def mouse_click(position,delay=0):
    MS_enter.position = position
    MS_enter.click(pynput.mouse.Button.left,1)
    if delay>0:
        time.sleep(delay)

def mouse_doublec(position, delay=0):
    MS_enter.position = position
    MS_enter.click(pynput.mouse.Button.left,2)
    if delay>0:
        time.sleep(delay)


def key_strtype(e_string):
    KB_enter.type(e_string)

def key_press(key):
    KB_enter.press(key)
    KB_enter.release(key)


def date_string(date_start, time_delta):
    global date_initial
    date_end = date_start - timedelta(days=1)
    date_begin = date_start - timedelta(days=time_delta)
    date_initial = date_begin
    return ['{0:02d}/{1:02d}/{2:02d}'.format(date_begin.month,date_begin.day,date_begin.year%100), '{0:02d}/{1:02d}/{2:02d}'.format(date_end.month,date_end.day,date_end.year%100), '{0}{1:02d}{2:02d}-{3}{4:02d}{5:02d}'.format(date_begin.year,date_begin.month,date_begin.day,date_end.year,date_end.month,date_end.day )]


def file_name(directory, name):
    return directory+'\\'+name


def existing_file(directory, name, exten_name):
    full_name = name + exten_name
    if full_name in os.listdir(directory):
        return True
    else:
        return False

def date_ret(str_date):
    list_date = str_date.split("/")
    year = "20" + list_date[2]
    return year + list_date[0] + list_date[1]

#### pdf and xls pair record ###
pair_record = open("miss_pairs.txt","w",encoding="utf-8",errors="ignore")
print("Start\tEnd\tOrder\tPDF\tXLS", file=pair_record)


with open("file_record.txt", "r", encoding= "utf-8", errors="ignore") as record_file:
    record_obj = record_file.readlines()
    for item in record_obj[1:]:
        item_list = item.split("\t")
        date_1, date_2 = item_list[0], item_list[1]
        date_name = date_ret(date_1) + "-" + date_ret(date_2)
        report_number = int(item_list[2])
        if report_number%50!=0:
            report_page = report_number//50 + 1
        else:
            report_page = report_number//50
        for loop_time in range(report_page):
            order_num = str(loop_time+1)
            f_file = date_name+'_'+order_num
            missing_xls = 0
            missing_pdf = 0
            if not existing_file(index_dir, f_file, ".xls"):
                missing_xls = 1
            if not existing_file(call_dir,f_file,".pdf"):
                missing_pdf = 1
            if missing_xls + missing_pdf ==2:
                print("%s\t%s\t%s\t%d\t%d"%(date_1,date_2,order_num,1,1), file=pair_record)
            elif missing_xls == 1:
                print("%s\t%s\t%s\t%d\t%d"%(date_1,date_2,order_num,0,1), file=pair_record)
            elif missing_pdf == 1:
                print("%s\t%s\t%s\t%d\t%d"%(date_1,date_2,order_num,1,0), file=pair_record)

            
        
        




