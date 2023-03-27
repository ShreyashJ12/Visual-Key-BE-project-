from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, messagebox
from PIL import ImageTk,Image
from pathlib import Path
from vkdatabaseconnect import checkUser

from Register import register_window
from SelectImages import selectimg_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class login_window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
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

        self.canvas.place(x = 0, y = 0)

        self.img = Image.open(relative_to_assets("bg-img1.png"))
        self.background_image = ImageTk.PhotoImage(self.img) 
        self.canvas.create_image(0, 0, anchor='nw', image= self.background_image) 


        self.canvas.create_text(
            288.0,
            213.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Kalam", 64 * -1)
        )

        self.RegisterImg = ImageTk.PhotoImage(Image.open(relative_to_assets("login_register.png")))
        Registerbutton = self.canvas.create_image(435.0, 652.0, image=self.RegisterImg)
        self.canvas.tag_bind(Registerbutton, "<Button-1>", self.open_register_window)


        self.canvas.create_text(
            250.0,
            632.0,
            anchor="nw",
            text="New User?",
            fill="#FFFFFF",
            font=("Kalam", 18, "bold")
        )

        self.LoginImg = ImageTk.PhotoImage(Image.open(relative_to_assets("login.png")))
        Loginbutton = self.canvas.create_image(360, 548, image=self.LoginImg)
        self.canvas.tag_bind(Loginbutton, "<Button-1>", self.checkusr)

        self.username = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            font = ("18")
        )
        self.username.place(
            x=140.0,
            y=435.0,
            width=449.0,
            height=53.0
        )

        self.canvas.create_text(
            140.0,
            388.0,
            anchor="nw",
            text="Username",
            fill="#72E1F9",
            font=("Kalam", 32 * -1)
        )



    def open_register_window(self, event):
        register = register_window(self)
        register.show()
        self.hide()

    def checkusr(self, event):
        if checkUser(self.username.get()):
            self.open_selectimg_window()
        else:
            messagebox.showerror("Error", "User does not exist")
            self.username.delete(0, 'end')



    def open_selectimg_window(self):
        selectimg = selectimg_window(self, self.username.get())
        selectimg.show()
        self.hide()
    

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()