from tkinter import *
import random
import time
import threading

def run():
    
    # def autoClose():
    #     for i in range(10):
    #         time.sleep(1)
    #     win.destroy()

    win = Tk()
    win.title("一詞多譯")
    win.geometry('500x500+700+300')
    win.configure(background='white')


    #Label
    launch = Label(text="", bg="white")
    launch.pack()

    #CheckBox
    checkVar1 = IntVar() 
    cbox1 = Checkbutton(win, variable=checkVar1, text="")
    cbox1.pack()

    #Button
    btn = Button(text="確定", bg="skyblue")
    # btn.config()
    btn.pack()

    # t=threading.Thread(target=autoClose) 
    # t.start()
    win.mainloop()

if __name__=='__main__':
    run()