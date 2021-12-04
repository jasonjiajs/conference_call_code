#### This is the most updated code for automatically downloading conference calls from Thomson One Streetevents
#### The position need to be adjusted by using "mouse_key_recorder.py"
#### This code ensures that lists and pdfs come in pairs and do not need further adjustments
#### The database is changing itself. So it's always best to download the pairs of lists and pdfs together (sometimes there might be errors)

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
call_dir = r"C:\Users\stang10\ConferenceCall\CallScripts5"
index_dir = r"C:\Users\stang10\ConferenceCall\List5"


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

#### mouse click list one: put start date and end date for each loop
#### 1: click start date  2: erase start date  3: click end date  4: erase end date 5: get the number of reports being searched
mouse_c_list_1 = [(381, 373), (428, 376), (541, 375), (584, 378), (146,788)] ###[(397, 459), (426, 462), (543, 454), (584, 454)]
mouse_c_list_2 = [(32, 852), [(1678, 788),(1712, 788)], (1315, 1019), (1348, 992), (56, 819), (557, 321), (554, 764), (32, 852), (1854, 786)]
### [(29, 941), (2360, 871), (2011, 1316), (2071, 1279), (57, 907), (888, 522), (890, 971),(1197,214), (1344, 176), (31, 941), (2496, 875)]

#### put end date here
date_initial = datetime.date(year=2020, month=10, day=26)

record_file = open("C:\\Users\\stang10\\ConferenceCall\\file_number.txt", "w", encoding="utf-8", errors="ignore")
print("Start date\tEnd date\tNo. Reports", file=record_file)

click_time = 0
error_time = 0

while date_initial > datetime.date(year=2020, month=10, day=24):
    if error_time >= 200 and click_time>=0:
        if error_time >= 500:
            print("The date %s to %s, page %d is damaged"%(date_list[0], date_list[1], click_time+1)) # give this message and try next page
            click_time = click_time + 1
            print(click_time)
        if click_time>=report_page:
            click_time = 0
            error_time = 0
    elif error_time >= 3500 and click_time==-1:
        print("break point! Stop now")
        break
    if click_time==0 and error_time==0:
        date_list = date_string(date_initial,2)
    mouse_click(mouse_c_list_1[0],0.5)
    mouse_click(mouse_c_list_1[1],0.5)
    key_strtype(date_list[0])
    time.sleep(0.5)
    mouse_click(mouse_c_list_1[2],0.5)
    mouse_click(mouse_c_list_1[3],0.5)
    key_strtype(date_list[1])
    time.sleep(0.5)

    key_press(Key.enter) ### search results displayed for the time period
    time.sleep(8)
    
    # get the number of reports being searched
    mouse_doublec(mouse_c_list_1[4],0.5)
    ## copy the number
    with KB_enter.pressed(Key.ctrl):
        key_press('c')
    time.sleep(0.5)
    ### read from clipboard the copied number
    report_number = pyperclip.paste()
    try:
        report_number = int(report_number)
        print("%s\t%s\t%d"%(date_list[0],date_list[1],report_number), file=record_file)
    except ValueError:
        if report_number=="query":
            report_number = 0
            print("%s\t%s\t%d"%(date_list[0],date_list[1],report_number), file=record_file)
        else:
            mouse_click((1862,546),2)
            mouse_click((291,44),2)
            key_strtype(r"http://proxy.uchicago.edu/login/thomsonone")
            time.sleep(0.5)
            key_press(Key.enter)
            time.sleep(30)
            #### now we have to click to to search screen
            mouse_click((644,95),2)
            mouse_click((302,120),10)
            mouse_click((99,626),2)
            ## type in source
            key_strtype("STREETEVENTS")
            time.sleep(3)
            mouse_click((93,669),3)
            click_time = -1
            continue
    pyperclip.copy("")
    if report_number%50!=0:
        report_page = report_number//50 + 1
    else:
        report_page = report_number//50
    if report_page>40:
        print("%d pages for date %s to %s"%(report_page, date_list[0],date_list[1]))
        report_page = 40

    for loop_time in range(report_page):
        if loop_time < click_time:
            print(loop_time,click_time)
            mouse_click(mouse_c_list_2[8], 5) 
            continue
        ## page_number here
        order_num = str(loop_time+1)
         ### select all reports
        mouse_click(mouse_c_list_2[0], 1)





        ### now get the report
        #### check first whether it is already
        f_file = date_list[2]+'_'+order_num
        f_name = file_name(call_dir, date_list[2]+'_'+order_num)
        if not existing_file(call_dir,f_file,".pdf"):
            file_num1 = len(os.listdir(call_dir))
            file_num2 = file_num1
            ## i. Click on the View icon

            mouse_click(mouse_c_list_2[4],8)
            ## ii. Click the select and view icon
            mouse_click(mouse_c_list_2[5],1)
            mouse_click(mouse_c_list_2[6],15)
            start_time = time.time()
            while file_num2==file_num1:
            ## iii. Wait for the report to come out, type shift + ctrl + s to save
                with KB_enter.pressed(Key.shift, Key.ctrl):
                    key_press('s')
                ## iv. Type the file name
                time.sleep(3)
                key_strtype(f_name)
                time.sleep(0.5)
                key_press(Key.enter)
                time.sleep(6)
                ## see if there is a new file there, if not, continue to do this loop
                file_num2 = len(os.listdir(call_dir))
                end_time = time.time()
                if end_time - start_time>=300 and file_num2==file_num1: # if inactivity logout, need to restart the procedure and do everything
                    if end_time - start_time>=500:
                        error_time = error_time + end_time - start_time
                        break
                    else:
                        mouse_click(mouse_c_list_2[5],5)
                        mouse_click(mouse_c_list_2[6],15)


            ## handle error logout
            if end_time - start_time>=300 and file_num2==file_num1:
                mouse_click((1862,546),2)
                mouse_click((291,44),2)
                key_strtype(r"http://proxy.uchicago.edu/login/thomsonone")
                time.sleep(0.5)
                key_press(Key.enter)
                time.sleep(30)
                #### now we have to click to to search scree
                # n
                mouse_click((644,95),2)
                mouse_click((302,120),10)
                mouse_click((99,626),2)
                ## type in source
                key_strtype("STREETEVENTS")
                time.sleep(3)
                mouse_click((93,669),3)
                click_time = loop_time
                break
            


            ### restart from the break point    


            ## v. Close the window by typing Alt+F4
            with KB_enter.pressed(Key.alt):
                key_press(Key.f4)
            time.sleep(2)
            with KB_enter.pressed(Key.alt):
                key_press(Key.f4)

            mouse_click((1862,546),2)

            error_time = 0

                ### get the excel(maybe at multiple locations and as a result, we must try multiple positions)

        ## i. Click on the excel icon
        #### check if the name saved is already there
        f_file = date_list[2]+'_'+order_num
        f_name = file_name(index_dir, date_list[2]+'_'+order_num)
        if not existing_file(index_dir, f_file, ".xls"):
            start_time = time.time()
            while not existing_file(index_dir, f_file, ".xls"):
                if report_number>50:
                    mouse_click(mouse_c_list_2[1][0],8)
                else:
                    mouse_click(mouse_c_list_2[1][1],8)
                ## ii. Select save annd save as
                mouse_click(mouse_c_list_2[2],2)
                mouse_click(mouse_c_list_2[3],8)
                ## iii. Enter the name of the excel and save it
                key_strtype(f_name)
                time.sleep(2)
                key_press(Key.enter)
                time.sleep(1)
                ### cancel and redo
                mouse_click((1424,1020),3)
                end_time = time.time()
                if end_time - start_time>=200 and not existing_file(index_dir, f_file, ".xls"): # if inactivity logout, need to restart the procedure and do everything
                    error_time = error_time + end_time - start_time
                    break
        
            if end_time - start_time>=200 and not existing_file(index_dir, f_file, ".xls"):
                mouse_click((1862,546),2)
                mouse_click((291,44),2)
                key_strtype(r"http://proxy.uchicago.edu/login/thomsonone")
                time.sleep(0.5)
                key_press(Key.enter)
                time.sleep(30)
                #### now we have to click to to search screen
                mouse_click((644,95),2)
                mouse_click((302,120),10)
                mouse_click((99,626),2)
                ## type in source
                key_strtype("STREETEVENTS")
                time.sleep(3)
                mouse_click((93,669),3)
                click_time = loop_time
                break  

        ### dis select the reports
        mouse_click(mouse_c_list_2[7], 0.5)
        ### next page
        mouse_click(mouse_c_list_2[8], 5)          
        #### reset click_time
        click_time = 0
        ### reset error_time
        error_time = 0
    

### some problems
### the new page and the excel key will move with different number of observations
### close page, and wait for the page to refresh will take some time.
### Make sure that different number of reports will not affect the place of  (next page versus excel)