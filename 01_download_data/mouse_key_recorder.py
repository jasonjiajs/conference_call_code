######## Utility: this python file serves to record the mouse position you wanna click ######
######## type Shift if you want to record a mouse position #####
######## type Esc if you want to stop, and will return a list of all the mouse positions you have clicked ####

import pynput
import time

###### we wanna record all the position we need to click and the key we wanna use ########
position_list = []
def record_position(p_list,x,y):
    p_list.append((x,y))
    return p_list

#### key board listener ###
def on_press(key):
    if (key==pynput.keyboard.Key.shift):
        with pynput.mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
            listener.join()

def on_release(key):
    if key== pynput.keyboard.Key.esc:
        return False

#### mouse listener #####
def on_move(x,y):
    pass

def on_click(x, y, button, pressed):
    global position_list
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x,y)))
    if pressed:
        position_list=record_position(position_list,x,y)
    if not pressed:
        return False

def on_scroll(x,y,dx,dy):
    print('Scrolled {0}'.format((x,y)))

with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as klistener:
    klistener.join()


def mouse_click(mouse,position,delay):
    mouse.position = position
    mouse.click(pynput.mouse.Button.left,1)
    time.sleep(delay)


print(position_list)


