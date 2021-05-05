from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger


translations_dic = {} 
def add_translations(multiple_translation_words, translations):
    # logger.warn(multiple_translation_words)
    # logger.warn(translations)
    if type(translations[0]) == list:
        # logger.warn("yes")
        translations = translations[0]
    for i in range(len(multiple_translation_words)): #看有幾個有一詞多譯的字
        translations_dic[multiple_translation_words[i]] = translations
    logger.warn(translations_dic)

def run():
    def show_translations_dic():
        if translations_dic :
            first_key = list(translations_dic)[0]
            for i, data in enumerate(translations_dic[first_key]):
                # logger.warn(data)
                if i==0:
                    ctext1.set(data)
                elif i==1:
                    ctext2.set(data)
            # logger.warn(trans_options)
            text1.set("%s 可以被翻譯成: " % first_key)

    def output_setting_file():
        with open("code/listeners/setting.txt", "a") as out_file:
            contents = ""
            if checkVar1.get() == 1:
                contents = list(translations_dic)[0] + ":" + ctext1.get() + "\n"
            else:
                contents = list(translations_dic)[0] + ":" + ctext2.get() + "\n"
            logger.warn(contents)
            out_file.write(contents)
            win.destroy()

    win = Tk()    

    win.title("一詞多譯")
    # win.geometry('500x500+700+300')
    canvas = Canvas(win, width=300, height=500)
    canvas.grid(columnspan=3, rowspan=3)

    # 譯logo Image 
    logo = Image.open('code/gui/logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(image = logo)
    logo_label.image = logo
    logo_label.grid(columnspan=3, row=0, sticky=N+W+E)

    # 待翻譯字 Label
    ctext1 = StringVar()
    ctext2 = StringVar()
    text1 = StringVar()
    interpretation = Label(win, textvariable=text1, command= show_translations_dic(), font="Raleway")
    interpretation.grid( column=0, row=1, sticky=W+N)
    
    # 一詞多譯選項 Radiobutton
    checkVar1 = IntVar() 
    cbox1 = Radiobutton(win, variable=checkVar1, textvariable=ctext1, font="Raleway", value=1)
    cbox1.grid(column=1, row=1, sticky=W+N)

    cbox2 = Radiobutton(win, variable=checkVar1, textvariable=ctext2, font="Raleway", value=0)
    cbox2.grid(column=2, row=1, sticky=W+N)

    # 標語 Label
    instructions = Label(win, text="Choose the translation(s) you want!!", font="Raleway")
    instructions.grid(row=6, sticky=S+W)

    # 提交 Button
    text = StringVar()
    btn = Button(win, textvariable=text, command= lambda:output_setting_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    text.set("Submit")
    btn.grid(row=6,column=2, sticky=S+E)

    # canvas = Canvas(win, width=600, height=300)
    # canvas.grid(columnspan=3, rowspan=3)

    # t=threading.Thread(target=autoClose) 
    # t.start()
    win.mainloop()

if __name__=='__main__':
    run()