from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger
import tkinter.font as tkFont
import os


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
        with open("i18n/listeners/setting.txt", "a") as out_file:
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

            # 把已輸入的資料和 submit btn 在ui上隱藏
            for i in range(len(self.labels)):
                self.labels[i].grid_forget()
                self.labels_word[i].grid_forget()
                for j in range(len(self.radios[i])):
                    self.radios[i][j].grid_forget()
            self.btn_submit.grid_forget()
            # self.win.destroy()
    
    def undo_trans(self):
        with open("i18n/listeners/setting.txt", "a+") as modi_file:
            if os.stat("i18n/listeners/setting.txt").st_size != 0:
                modi_file.seek(0)  #這行很重要，將指針指到文件頭

                #先準備要清除的資料
                content_rmv = []
                for i in range(len(self.checkbtn_vars)):
                    # logger.warn(self.checkbtn_vars[i].get())
                    if self.checkbtn_vars[i].get() == 1:
                        content_rmv.append(self.checkbtn_texts[i]+'\n')
                # logger.warn(content_rmv)
                
                #開始掃描設定檔，並刪除符合的資料
                new_data = ""
                for line in modi_file.readlines():
                    if line not in content_rmv:
                        #這邊似乎無法直接修改值成""，所以最後採用覆寫的方式
                        new_data += line
                modi_file.seek(0)
                modi_file.truncate()
                modi_file.write(new_data)       
            #關閉record視窗
            self.record_ui.destroy()

    def draw_trans_options(self):
        self.labels = []

        self.labels_word = []
        self.label_texts = []

        self.radios = []
        self.radio_vars = []
        self.radio_texts = []
        self.get_transdic_keys_and_values()
        for i in range(len(self.label_texts)): #根據有幾列label 來印出'完整參數&label'&'radiobtn'
            self.radio_vars.append(IntVar())
            # logger.warn(self.radio_vars)
            self.radios.append([])
            self.labels.append(Label(self.win, text="完整參數是:%s  ," % 
            (UI.origin_xpaths_or_arguments[i]), font=self.fontStyle)) #創出label(s)
            self.labels[i].grid( column=0,row=i, sticky=W+N+S, padx=10, pady=3)

            self.labels_word.append(Label(self.win, text="%s可以被翻譯成: " % 
            (self.label_texts[i]), font=self.fontStyle, fg = "red")) #創出label(s)
            self.labels_word[i].grid( column=1,row=i, sticky=W+N+S, padx=10, pady=3)

            #create出每一列中的radio button
            for j in range(len(self.radio_texts[i])):
                default_value = j
                self.radios[i].append(Radiobutton(self.win, variable=self.radio_vars[i], text=self.radio_texts[i][j], font=self.fontStyle, value=default_value))
                self.radios[i][j].grid(columnspan=1, column=2+j, row=i, sticky=W+N+S, pady=3)

    def open_record(self):
        self.record_ui = Toplevel(self.win)

        #ui基礎設定
        self.record_ui.title("使用者翻譯紀錄")
        self.record_ui.geometry('+250+250')

        #讀取setting.txt的內容，並列出
        with open("i18n/listeners/setting.txt", 'a+') as file:
            if os.stat("i18n/listeners/setting.txt").st_size != 0:
                file.seek(0)  #這行很重要，將指針指到文件頭

                #準備好checkbox資訊
                self.checkbtns = []
                self.checkbtn_vars = []
                self.checkbtn_texts = []
                for line in file.readlines():
                    self.checkbtn_texts.append(line.strip('\n'))
                    # logger.warn(line)
                
                #根據有幾筆資料，來創出checkbox
                for i in range(len(self.checkbtn_texts)):
                    self.checkbtn_vars.append(IntVar())
                    self.checkbtns.append(Checkbutton(self.record_ui, variable=self.checkbtn_vars[i], text=self.checkbtn_texts[i], font=self.fontStyle, \
                                                        bg='light green'))
                    self.checkbtns[i].grid(column=0, row=i, sticky=W+N+S, padx=10, pady=3)
            
            # Undo Button
            text_undo = StringVar()
            btn_undo = Button(self.record_ui, textvariable=text_undo, command= self.undo_trans, font=self.fontStyle, bg="#ff8a15", fg="white", height=1, width=8)
            text_undo.set("Undo")
            btn_undo.grid(row=10, column=0, sticky=S+E, padx=10, pady=5, columnspan=3)

    def run(self):
        self.win = Tk()    
        # logger.warn("tk")
        self.win.title("一詞多譯")
        self.win.geometry('+200+300')
        # canvas = Canvas(self.win, width=200, height=200)
        # canvas.grid(rowspan=2)
        
        self.fontStyle = tkFont.Font(family ="Helvetica", size=14)
        self.draw_trans_options()
        
        # 標語 Label
        self.instructions = Label(self.win, text="Choose the translation(s) you want!!", font=self.fontStyle)
        self.instructions.grid(row=10, sticky=S+W, padx=10, pady=5)

        # 顯示紀錄 Button
        self.text_record = StringVar()
        self.btn_record = Button(self.win, textvariable=self.text_record, command= self.open_record, font=self.fontStyle, bg="#8c4646", fg="white", height=2, width=15)
        self.text_record.set("TransRecord")
        self.btn_record.grid(row=10, column=1, sticky=S+E, padx=10, pady=5)

        # 提交 Button
        self.text_submit = StringVar()
        self.btn_submit = Button(self.win, textvariable=self.text_submit, command= lambda:self.output_setting_file(), font=self.fontStyle, bg="#20bebe", fg="white", height=2, width=15)
        self.text_submit.set("Submit")
        self.btn_submit.grid(row=10, column=2, sticky=S+E, padx=10, pady=5, columnspan=10)

        self.win.mainloop()



  
if __name__=='__main__':
    self.run()