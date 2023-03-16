import tkinter as tk
from tkinter import *
from tkinter import filedialog
from feature_extraction import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import hashlib
import aes256encrypt as aes256
from vkdatabaseconnect import addUser, saveImg

test_gui = tk.Tk()
test_gui.geometry("1920x1080")  # Size of the window
test_gui.title('TEST gui')
my_font1 = ('times', 18, 'bold')
num = IntVar(test_gui)
desc = StringVar(test_gui)
test = []
name = []
buttons = [] # to store button references


MainFrame = Frame(test_gui)
MainFrame.grid()

DataFrameLEFT = LabelFrame(MainFrame, bd=10, width=960, height=900, padx=20, relief=RIDGE)
DataFrameLEFT.pack(side=LEFT)

UpperHalf = LabelFrame(DataFrameLEFT, bd=10, width=960, height=300, padx=20, relief=RIDGE)
UpperHalf.pack(side=TOP)
                   
LowerHalf = LabelFrame(DataFrameLEFT, bd=10, width=920, height=600, padx=20, relief=RIDGE)
LowerHalf.pack(side=BOTTOM)

DataFrameRIGHT = LabelFrame(MainFrame, bd=10, width=960, height=900, padx=20, relief=RIDGE)
DataFrameRIGHT.pack(side=RIGHT)

lbl = Label(UpperHalf, text="Enter a username", width=30, font=my_font1)
lbl.grid(row=1, column=1)
username = Entry(UpperHalf, width=50, font=my_font1)
username.grid(row=2, column=1)

l1 = tk.Label(UpperHalf, text='Uploading the images', width=30, font=my_font1)
l1.grid(row=3, column=1, columnspan=4)
b1 = tk.Button(UpperHalf, text='Upload Files', width=20, command=lambda: upload_file())
b1.grid(row=4, column=1, columnspan=4)

lbl = Label(DataFrameRIGHT, text="Enter number of images for your password:", width=30, font=my_font1)
lbl.grid(row=1, column=1)
image_label = Scale(DataFrameRIGHT, from_=3 , to=9, orient=tk.HORIZONTAL, length=150, showvalue=0, tickinterval=1, resolution=1, variable = num)
image_label.grid(row=2, column=1)

lbl = Label(DataFrameRIGHT, text="Sentence generated:", width=30, font=my_font1)
lbl.grid(row=3, column=1)
image_label = Entry(DataFrameRIGHT, width=50, font=my_font1, textvariable=desc)
image_label.grid(row=4, column=1)

def show_img(imgnm):
    name.append(imgnm)
    print(imgnm)
    if len(name) == num.get():
        for i in range(len(buttons)):
            buttons[i].config(state="disabled")
        generate_desci(name)

def upload_file():
    f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'),
               ('PNG Files', '*.png')]  # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    global saveImage
    saveImage = tuple(filename)
    tuple(filename)
    print("Done")
    col = 1  # start from column 1
    row = 5  # start from row 3
    for f in filename:
        img = Image.open(f)  # read the image file
        img = img.resize((100, 100))  # new width & height
        img = ImageTk.PhotoImage(img)
        btn = tk.Button(LowerHalf, text=filename.index(f), command=lambda imgf=f:show_img(imgf))
        btn.image = img
        btn['image'] = img
        btn.grid(row=row, column=col)
        buttons.append(btn)
        if col == 5:  # start new line after third column
            row = row + 1  # start with next row
            col = 1  # start with first column
        else:  # within the same row
            col = col + 1  # increase to next column

def generate_desci(filename):
    for f in filename:
        # load and prepare the photograph
        photo = extract_features(f)
        # generate description
        max_length = 33
        description = generate_desc(model, tokenizer, photo, max_length)
        test.append(clean_description(description))
    desc.set((" ").join(test))
    enc_it = " ".join(test)
    hashed_string = hashlib.sha256(enc_it.encode('utf-8')).hexdigest()
    passwd = aes256.encrypt(hashed_string, username.get())
    addUser(username.get(), passwd)
    saveImg(saveImage, username.get())



test_gui.mainloop()  # Keep the window open
