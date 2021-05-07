from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger
import tkinter.font as tkFont

class UI:
    translations_dic = {} 

    def __init__(self):
        self.run()

    def add_translations(self, multiple_translation_words, translations):
        # logger.warn(multiple_translation_words)
        # logger.warn(translations)
        if type(translations[0]) == list:
            # logger.warn("yes")
            translations = translations[0]
        for i in range(len(multiple_translation_words)): #看有幾個有一詞多譯的字
            UI.translations_dic[multiple_translation_words[i]] = translations
        # logger.warn(translations_dic)

    def show_translations_dic(self):
        if UI.translations_dic :
            first_key = list(translations_dic)[0]
            for i, data in enumerate(translations_dic[first_key]):
                # logger.warn(data)
                if i==0:
                    ctext1.set(data)
                elif i==1:
                    ctext2.set(data)
            # logger.warn(trans_options)
            text1.set("%s 可以被翻譯成: " % first_key)
    
    def output_setting_file(self):
        with open("code/listeners/setting.txt", "a") as out_file:
            contents = ""
            if checkVar1.get() == 1:
                contents = list(UI.translations_dic)[0] + ":" + ctext1.get() + "\n"
            else:
                contents = list(UI.translations_dic)[0] + ":" + ctext2.get() + "\n"
            logger.warn(contents)
            out_file.write(contents)
            self.win.destroy()

    def draw_trans_options(self):
        self.labels = []
        self.radios = []
        self.radio_texts = []
        # self.radio_vars = []
        # self.ltexts = []
        for i in range(3): #先預設有3列 label
            # check_radio = StringVar()
            # self.radio_vars.append(check_radio)
            # radio_text_row = []
            # rtext1 = StringVar()
            # rtext2 = StringVar()
            # temp.append(rtext1, rtext2)
            # self.rtexts.append(temp)

            self.labels.append(Label(self.win, text='dict key'))
            self.labels[i].grid(column=0, row=i, sticky=W+N)
            #這邊要去create出每一列中的radio button
            for j in len(radio_texts[i]):
            #     if j==0:
            #         default_value = 1
            #     else: 
            #         default_value = 0
            #     samerow_radio = []
            #     self.samerow_radio.append(Radiobutton(self, variable=radio_vars[i], textvariable=temp[j], value=default_value ))
    def run(self):
        self.win = Tk()    
        # logger.warn("tk")
        self.win.title("一詞多譯")
        # win.geometry('500x500+700+300')
        canvas = Canvas(self.win, width=300, height=500)
        canvas.grid(columnspan=3, rowspan=3)
        
        self.draw_trans_options()
        fontStyle = tkFont.Font(family ="Raleway", size=20)
        # # 待翻譯字 Label
        # ctext1 = StringVar()
        # ctext2 = StringVar()
        # text1 = StringVar()
        # interpretation = Label(win, textvariable=text1, command= show_translations_dic(), font=fontStyle)
        # interpretation.grid( column=0, row=0, sticky=W+N)
        
        # # 一詞多譯選項 Radiobutton
        # checkVar1 = IntVar() 
        # cbox1 = Radiobutton(win, variable=checkVar1, textvariable=ctext1, font=fontStyle, value=1)
        # cbox1.grid(column=1, row=0, sticky=W+N)

        # cbox2 = Radiobutton(win, variable=checkVar1, textvariable=ctext2, font=fontStyle, value=0)
        # cbox2.grid(column=2, row=0, sticky=W+N)

        # 標語 Label
        instructions = Label(self.win, text="Choose the translation(s) you want!!", font=fontStyle)
        instructions.grid(row=6, sticky=S+W)

        # 提交 Button
        text = StringVar()
        btn = Button(self.win, textvariable=text, command= lambda:self.output_setting_file(), font=fontStyle, bg="#20bebe", fg="white", height=2, width=15)
        text.set("Submit")
        btn.grid(row=6,column=2, sticky=S+E)

        self.win.mainloop()

if __name__=='__main__':
    self.run()