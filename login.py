import os
import random
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from feature_extraction import *
from PIL import Image, ImageTk
import hashlib
import aes256encrypt as aes256

root = tk.Tk()
root.geometry("1920x1080")  # Size of the window
root.title('Login')
USERNAME = StringVar()
buttons = []

def user_login():
    if USERNAME.get() == "shreyash":
        root.withdraw()
        usl = Toplevel()
        usl.title("Enter password")
        usl.geometry('1920x1080+0+0')
        col = 1  # start from column 1
        row = 5  # start from row 3
        name = []
        num = 3
        Title = Frame(usl, bg='powder blue')
        Title.pack()

        PassFrame = LabelFrame(usl, bd=10, width=560, height=500, padx=20, relief=RIDGE, )
        PassFrame.pack()

        lbl_title = Label(Title, text="Select the correct images", font=('arial', 11, 'bold')).grid(row=0, column=0)

        def show_img(path, imgnm):
            name.append(os.path.join(path,imgnm))
            print(name)
            if len(name) == num:
                for i in range(len(buttons)):
                    buttons[i].config(state="disabled")
                generate_desci(name)

        def generate_desci(filename):
            for f in filename:
                # load and prepare the photograph
                photo = extract_features(f)
                # generate description
                max_length = 33
                description = generate_desc(model, tokenizer, photo, max_length)
                description = clean_description(description)
            hashed_string = hashlib.sha256(description.encode('utf-8')).hexdigest()
            print("hashed sentence:", hashed_string)
            test = "1GJIV1YICKxwLTLaoFsy0Gr4jOJ62fpXGwCRrbKNZSDJsSNgDRT2fEAiArz1NU1opSeeA1N1QofrCeuJon5c8w=="
            print(aes256.encrypt(hashed_string, "shreyash")['cipher_text'])
            if aes256.encrypt(hashed_string, "shreyash")['cipher_text'] == test:
                tkinter.messagebox.showinfo("Success", "Logged in successfully")
            else:
                tkinter.messagebox.showerror("Error", "The entered credentials are incorrect")
                usl.destroy()
                root.deiconify()

        folderpath = r"./test images"
        filename = os.listdir(folderpath)
        random.shuffle(filename)
        for f in filename:
            img = Image.open(os.path.join(folderpath,f))  # read the image file
            img = img.resize((100, 100))  # new width & height
            img = ImageTk.PhotoImage(img)
            btn = tk.Button(PassFrame, text=filename.index(f), command=lambda imgf=f:show_img(folderpath, imgf))
            btn.image = img
            btn['image'] = img
            btn.grid(row=row, column=col)
            buttons.append(btn)
            if col == 5:  # start new line after third column
                row = row + 1  # start with next row
                col = 1  # start with first column
            else:  # within the same row
                col = col + 1  # increase to next column



frame = Frame(root, bg='powder blue')
frame.pack()

Title = Frame(root, bg='powder blue')
Title.pack()

Details = Frame(root, bg='powder blue')
Details.pack()

lbl_title = Label(Title, text="Login", font=('arial', 14, 'bold')).grid(row=0, column=0)

username = Entry(Details, textvariable=USERNAME, font=('arial', 15, 'bold'))
username.grid(row=0, column=0)

b2 = Button(Details, text="Next", font=('arial', 11, 'bold'), width=10, height=2, command = user_login).grid(row=1, column=0)

mainloop()