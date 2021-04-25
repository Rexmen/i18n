import tkinter as tk

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('BMI App')
window.geometry('800x600')
window.configure(background='white')

#Function
def confirm_choice():
    print("Choice have saved!")

#Label
title = tk.Label(text="i18n工具偵測到了一詞多譯:")
title.pack()
trans = tk.Label(text="Support可翻譯成:")
trans.pack()

#checkbox
cbox = tk.Checkbutton(window, variable=0, text="支援")
cbox.pack()

#Button
btn = tk.Button(text="確定")
btn.config(bg="skyblue")
btn.config(command = confirm_choice)
btn.pack()

# 運行主程式
window.mainloop()