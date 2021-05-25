from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger
import tkinter.font as tkFont

class UI:
    translations_key = []
    translations_value = []
    origin_xpaths_or_arguments = []
    unique_log= []

    def __init__(self):
        self.run()

    def add_translations(self, multi_trans_word, translations, full_args):
        # logger.warn(multiple_translation_words)
        # logger.warn(translations)
        if not type(translations[0]) == list:  #因為傳進來的translations型態會隨著'要翻譯詞'數量而不同
            translations = [translations]      #兩個以上，translations是list包list; 一個，list
        # 下面這行是因為multiple_translation_words可能有許多筆要翻譯的詞，考慮到同一條xpath中有多處需要被翻譯
        # for i in range(len(multiple_translation_words)): 
        # FIXME 今後只支援一次記錄下一組翻譯資訊，為了配合底下的邏輯修改
        # 若findelementsProxy翻譯xpath時可能有多個翻譯詞的情形，則必須去改善自己的邏輯 可以參考 selectFromListByValue
        # 也就是說，日後每輸入一組翻譯，就必須同時輸入一次origin_xpaths_or_arguments
        
        #FIXME 因為dict會覆寫的特性，導致我們無法將 '不同情況下相同的翻譯詞' 顯示在UI上給user選擇
        # 希望改進成類似於讀取檔案時的寫法，把KEY VALUE分開儲存
        
        UI.translations_key.append(multi_trans_word[0])
        UI.translations_value.append(translations[0])
        UI.unique_log.append(str(full_args) + multi_trans_word[0])
        # logger.warn(UI.translations_key)
        # logger.warn(UI.translations_value)

    def get_transdic_keys_and_values(self):# FIXME 此function日後是否有存在的必要
        if UI.translations_key and UI.translations_value:
            for key in UI.translations_key:
                self.label_texts.append(key)
            for value in UI.translations_value:
                self.radio_texts.append(value)
                # logger.warn(label_texts)
    
    def output_setting_file(self):
        with open("code/listeners/setting.txt", "a") as out_file:
            contents = ""
            for i in range(len(self.label_texts)):
                now_selected = self.radio_vars[i].get()
                # logger.warn(now_selected)
                format_args=""
                for j in UI.origin_xpaths_or_arguments[i]:
                    format_args += j + "#"
                format_args = format_args[:-1]
                contents += format_args + "~" + self.label_texts[i] + "~" + self.radio_texts[i][now_selected] + "\n"
            logger.warn(contents)
            out_file.write(contents)
            self.win.destroy()

    def draw_trans_options(self):
        self.labels = []
        self.radios = []
        self.radio_vars = []
        self.radio_texts = []
        self.label_texts = []
        self.get_transdic_keys_and_values()
        for i in range(len(self.label_texts)): #根據有幾列label 來印出'完整參數&label'&'radiobtn'
            self.radio_vars.append(IntVar())
            # logger.warn(self.radio_vars)
            self.radios.append([])
            self.labels.append(Label(self.win, text="完整參數是:%s, %s可以被翻譯成: " % 
            (UI.origin_xpaths_or_arguments[i],self.label_texts[i]), font=self.fontStyle)) #創出label(s)
            self.labels[i].grid( column=0,row=i, sticky=W+N+S, padx=10, pady=3)
            #create出每一列中的radio button
            for j in range(len(self.radio_texts[i])):
                default_value = j
                self.radios[i].append(Radiobutton(self.win, variable=self.radio_vars[i], text=self.radio_texts[i][j],font=self.fontStyle, value=default_value ))
                self.radios[i][j].grid(columnspan=1, column=1+j, row=i, sticky=W+N+S, pady=3)
    
    def run(self):
        self.win = Tk()    
        # logger.warn("tk")
        self.win.title("一詞多譯")
        self.win.geometry('+200+300')
        canvas = Canvas(self.win, width=200, height=200)
        # canvas.grid(rowspan=2)
        
        self.fontStyle = tkFont.Font(family ="Helvetica", size=14)
        self.draw_trans_options()
        
        # 標語 Label
        instructions = Label(self.win, text="Choose the translation(s) you want!!", font=self.fontStyle)
        instructions.grid(row=6, sticky=S+W, padx=10, pady=5)

        # 提交 Button
        text = StringVar()
        btn = Button(self.win, textvariable=text, command= lambda:self.output_setting_file(), font=self.fontStyle, bg="#20bebe", fg="white", height=2, width=15)
        text.set("Submit")
        btn.grid(row=6,column=2, sticky=S+E,padx=10, pady=5)

        self.win.mainloop()

if __name__=='__main__':
    self.run()