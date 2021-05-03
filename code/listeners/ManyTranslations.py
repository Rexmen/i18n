from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger

translations_dic = {} 
show_trans_choice = ""

def add_translations(multiple_translation_words, translations):
    # logger.warn(multiple_translation_words)
    # logger.warn(translations)
    # logger.warn(len(multiple_translation_words))
    for i in range(len(multiple_translation_words)):
        translations_dic[multiple_translation_words[i]] = translations[i]
    # logger.warn(translations_dic)

def show_translations_dic():
    first_key = list(translations_dic)[0]
    trans_options = ""
    for i, data in enumerate(translations_dic[first_key]):
        trans_options+= data
        if i != len(translations_dic[first_key]) -1 :
            trans_options += " 或 "
    logger.warn(trans_options)
    show_trans_choice = "%s 可以被翻譯成 %s " % (first_key, trans_options)
    logger.warn(show_trans_choice)
    


def run():

    win = Tk()
    win.title("一詞多譯")
    # win.geometry('500x500+700+300')
    canvas = Canvas(win, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)

    #logo
    logo = Image.open('code/gui/logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(image = logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

    #label of 選擇區
    canvas = Canvas(win, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)
    text1 = StringVar()
    interpretation = Label(win, textvariable=text1, command= show_translations_dic(), font="Raleway")
    text1.set(show_trans_choice)
    interpretation.grid(columnspan=2, column=0, row=1)
    

    #Label
    instructions = Label(win, text="Choose a interpretation you want!!", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=2)

    #CheckBox
    # checkVar1 = IntVar() 
    # cbox1 = Checkbutton(win, variable=checkVar1, text="")
    # cbox1.pack()

    #Button
    text = StringVar()
    btn = Button(win, textvariable=text, font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text.set("Submit")
    btn.grid(column=1, row=3)


    # canvas = Canvas(win, width=600, height=300)
    # canvas.grid(columnspan=3, rowspan=3)

    # t=threading.Thread(target=autoClose) 
    # t.start()
    win.mainloop()

if __name__=='__main__':
    run()