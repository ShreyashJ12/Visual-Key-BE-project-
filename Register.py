from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, messagebox
from PIL import ImageTk,Image
from pathlib import Path
from vkdatabaseconnect import checkUser, addUser
import re
from CreatePass import createpass_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class register_window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("1417x878")
        self.configure(bg = "#0C464A")

        self.canvas = Canvas(
            self,
            bg = "#0D474B",
            height = 878,
            width = 1417,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.img = Image.open(relative_to_assets("bg-img1.png"))
        self.background_image = ImageTk.PhotoImage(self.img) 
        self.canvas.create_image(0, 0, anchor='nw', image= self.background_image) 

        self.canvas.place(x = 0, y = 0)

        self.LoginImg = ImageTk.PhotoImage(Image.open(relative_to_assets("register_login.png")))
        LoginImgbutton = self.canvas.create_image(488, 740, image=self.LoginImg)
        self.canvas.tag_bind(LoginImgbutton, "<Button-1>", self.open_login_window)


        self.canvas.create_text(
            184.0,
            714.0,
            anchor="nw",
            text="Already registered?",
            fill="#FFFFFF",
            font=("Kalam", 32 * -1)
        )

        self.CreatepassImg = ImageTk.PhotoImage(Image.open(relative_to_assets("register_createpass.png")))
        Createpassbutton = self.canvas.create_image(360, 651, image=self.CreatepassImg)
        self.canvas.tag_bind(Createpassbutton, "<Button-1>", self.createpasswd)


        self.email = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font = ("18")
        )
        self.email.place(
            x=75.0,
            y=473.0,
            width=539.0,
            height=71.0
        )

        self.canvas.create_text(
            75.0,
            422.0,
            anchor="nw",
            text="Enter your Email ",
            fill="#72E1F9",
            font=("Kalam", 32 * -1)
        )

        self.username = Entry(
            self,
            bd=0,
            bg="#FFFFF1",
            fg="#000716",
            highlightthickness=0,
            font = ("18")
        )
        self.username.place(
            x=75.0,
            y=311.0,
            width=539.0,
            height=71.0
        )

        self.canvas.create_text(
            75.0,
            257.0,
            anchor="nw",
            text="Enter Username",
            fill="#72E1F9",
            font=("Kalam", 32 * -1)
        )

        self.canvas.create_text(
            75.0,
            114.0,
            anchor="nw",
            text="Register",
            fill="#FFFFFF",
            font=("Kalam", 64 * -1)
        )

    def createpasswd(self, event):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if self.username.get() == "" or self.email.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif checkUser(self.username.get()):
            messagebox.showerror("Error", "Username already exists")
        elif re.fullmatch(regex, self.email.get()) is None:
            messagebox.showerror("Error", "Invalid Email")
        else:
            userid = addUser(self.username.get(), self.email.get())
            self.open_createpass_window(event, userid, self.username.get())

    def open_createpass_window(self, event, uid, name):
        createpass = createpass_window(self, uid, name)
        createpass.show()
        self.hide()
        
    def open_login_window(self, event):
        self.destroy()
        self.master.show()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()
