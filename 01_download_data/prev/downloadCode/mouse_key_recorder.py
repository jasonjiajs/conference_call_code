import pynput
import time



### mouth.scroll(0,4)


###### we wanna record all the position we need to click and the key we wanna use ########
position_list = []
def record_position(p_list,x,y):
    p_list.append((x,y))
    return p_list






#### key board listener ####




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
    mouse.click(Button.left,1)
    time.sleep(delay)

def main():
    mouse = Controller()
    select_p = (32,865) 
    mouse.position = select_p
    excel_p =  (1674,789)
    mouse.position = excel_p
    next_page_p = (1856,787)
    mouse.position = next_page_p
    save_p = (1278,1059)
    mouse.position = save_p

    #loop chane page and save it. 
    for i in range(1,10):
        mouse_click(mouse,select_p,1)
        mouse_click(mouse,excel_p,4)
        mouse_click(mouse,save_p,1)
        mouse_click(mouse,select_p,1)
        mouse_click(mouse,next_page_p,4.2)

# 1. open the page #http://proxy.uchicago.edu/login/thomsonone
# 2. Search conference call

print(position_list)


