from tkinter import *
from PIL import Image, ImageTk
# import PyPDF2
from tkinter.filedialog import askopenfile, asksaveasfile
import utils

def run():

    win = Tk()
    win.title("一詞多譯")


    canvas = Canvas(win, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)

    #logo
    logo = Image.open('./logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = Label(image = logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

    #instructions
    instructions = Label(win, text="Select a pdf file to extract all its text", font="Raleway")
    instructions.grid(columnspan=3, column=0, row=1)

    #functions 
    def open_file():
        browse_text.set("Loading...")
        file = askopenfile(parent=win, mode='rb', title="Choose a file", filetype=[("文字文件", "*.txt")], initialdir="C:/Users/petje/OneDrive/文件/")
        if file:
            text_box.delete("1.0" , "end")
            contents = file.readlines()
            count=0
            for line in contents:
                if count!=0:
                    text_box.insert(END, "\n")
                text_box.insert(END, line.strip())
                count+=1
            
        browse_text.set("Browse")
    
    def save_file():
        file= asksaveasfile(parent=win, title="Save", filetype=[("文字文件", "*.txt")], initialdir="C:/Users/petje/OneDrive/文件/")
        if file:
            contents = text_box.get("1.0" , "end-1c")
            # print(contents)
            file.write(contents)

    # textbox
    text_box = Text(win, height=10, width=50, padx=15, pady=15)
    text_box.grid(column=1, row=3)

    #Browse Button
    browse_text = StringVar()
    btn = Button(win, textvariable=browse_text, command=lambda:open_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
    browse_text.set("Browse")
    btn.grid(column=1, row=2)

    #save button
    save_btn = Button(win, text="save", command=lambda:save_file(), font="Raleway", bg="#20bebe", fg="white", height=2, width=10)
    save_btn.grid(column=2, row=3)

    canvas = Canvas(win, width=600, height=250)
    canvas.grid(columnspan=3)

    win.mainloop()

if __name__=='__main__':
    run()