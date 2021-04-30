from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk

def run():

    win = Tk()
    win.title("一詞多譯")
    # win.geometry('500x500+700+300')
    canvas = Canvas(win, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)

    #logo
    logo = Image.open('logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(image = logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

    #label of 選擇區
    canvas = Canvas(win, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)
    interpretation = Label(win, text="interpretation1", font="Raleway")
    interpretation.grid(columnspan=2, column=0, row=1)
    interpretation = Label(win, text="interpretation2", font="Raleway")
    interpretation.grid(columnspan=2, column=0, row=2)

    #Label
    instructions = Label(win, text="Choose a interpretation you want!!", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=3)

    #CheckBox
    # checkVar1 = IntVar() 
    # cbox1 = Checkbutton(win, variable=checkVar1, text="")
    # cbox1.pack()

    #Button
    text = StringVar()
    btn = Button(win, textvariable=text, font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text.set("Submit")
    btn.grid(column=1, row=4)


    # canvas = Canvas(win, width=600, height=300)
    # canvas.grid(columnspan=3, rowspan=3)

    # t=threading.Thread(target=autoClose) 
    # t.start()
    win.mainloop()

if __name__=='__main__':
    run()