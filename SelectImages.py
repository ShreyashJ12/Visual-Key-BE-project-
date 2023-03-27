from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Frame, messagebox
from PIL import ImageTk,Image
from feature_extraction import *
import hashlib
import aes256encrypt as aes256
from pathlib import Path
from vkdatabaseconnect import getImages, getPassword

from LoginSuccess import success_window
from ForgetPass import forgetpass_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class selectimg_window(Toplevel):

    def __init__(self, parent, user):
        self.user = user
        self.buttons = []
        super().__init__(parent)
        self.title("Login - Select Images")
        self.geometry("1417x878")
        self.configure(bg = "#0C464A")

        self.canvas = Canvas(
            self,
            bg = "#0C464A",
            height = 878,
            width = 1417,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        img = Image.open(relative_to_assets("bg-img1.png"))
        self.background_image = ImageTk.PhotoImage(img) 
        self.canvas.create_image(0, 0, anchor='nw', image= self.background_image) 

        self.canvas.place(x = 0, y = 0)

        self.ForgotPassImg = ImageTk.PhotoImage(Image.open(relative_to_assets("login_forgetpass.png")))
        ForgotPassImgbutton = self.canvas.create_image(1130, 770, image=self.ForgotPassImg)
        self.canvas.tag_bind(ForgotPassImgbutton, "<Button-1>", self.open_forgetpass_window)

        self.LoginImg = ImageTk.PhotoImage(Image.open(relative_to_assets("login_selectpass.png")))
        Loginbutton = self.canvas.create_image(1128, 670, image=self.LoginImg)
        self.canvas.tag_bind(Loginbutton, "<Button-1>", self.setTrue)


        self.canvas.create_text(
            54.0,
            25.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Kalam", 48 * -1)
        )

        # Create a frame
        self.imgframe = Frame(self.canvas, bg= "#151E28", width=784, height=790)
        # Add the frame to the self.canvas
        self.canvas.create_window(54.0, 92.0, window=self.imgframe, anchor="nw")


        filename = getImages(self.user)
        self.col = 1  # start from column 1
        self.row = 5 
        self.images = []

        def addImgs(imgn):
            self.images.append(imgn)

        for f in filename:
            pil_image = Image.fromarray(f)
            img = pil_image.resize((100, 100))  # new width & height
            img = ImageTk.PhotoImage(img)
            self.btn = Button(self.imgframe, command=lambda imgf=f: addImgs(imgf))
            self.btn.image = img
            self.btn['image'] = img
            self.btn.grid(row=self.row, column=self.col)
            self.buttons.append(self.btn)
            if self.col == 5:  # start new line after third column
                self.row = self.row + 1  # start with next row
                self.col = 1  # start with first column
            else:  # within the same row
                self.col = self.col + 1  # increase to next column
    
    def setTrue(self, event):
        for i in range(len(self.buttons)):
            self.buttons[i].config(state="disabled")
        print("Done")
        self.getDescription(self.images)

    def getDescription(self, images):
        test = []
        for f in images:
            # load and prepare the photograph
            #img = Image.fromarray(f)
            photo = extract_features(f)
            # generate description
            max_length = 33
            description = generate_desc(model, tokenizer, photo, max_length)
            test.append(clean_description(description))
        enc_it = " ".join(test)
        print(enc_it)
        hashed_string = hashlib.sha256(enc_it.encode('utf-8')).hexdigest()


        if hashed_string == aes256.checkpass(self.user):
            messagebox.showinfo("Success", "Login Successful")
            self.open_success_window()
        else:
            messagebox.showerror("Error", "Wrong Password")
            del self.images[:]
            for i in range(len(self.buttons)):
                self.buttons[i].config(state="normal")

    def getImage(user):
        images = getImages(user)
        return images
    
    
    def open_success_window(self):
        success = success_window(self)
        success.show()
        self.hide()

    def open_forgetpass_window(self, event):
        forgetpass = forgetpass_window(self)
        forgetpass.show()
        self.hide()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()
