from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from PIL import ImageTk,Image
from pathlib import Path
from genotp import rand_pass
from CreatePass import createpass_window
from vkdatabaseconnect import getUserfromMail

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class forgetpass_window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reset password")
        self.geometry("1417x878")
        self.configure(bg = "#0C464A")

        self.canvas = Canvas(
            self,
            bg = "#0C464A",
            height = 1024,
            width = 1440,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        img = Image.open(relative_to_assets("bg-img1.png"))
        self.background_image = ImageTk.PhotoImage(img) 
        self.canvas.create_image(0, 0, anchor='nw', image= self.background_image) 

        self.canvas.place(x = 0, y = 0)

        self.sendotpImg = ImageTk.PhotoImage(Image.open(relative_to_assets("sendotp.png")))
        sendotpbutton = self.canvas.create_image(721, 715, image=self.sendotpImg)
        self.canvas.tag_bind(sendotpbutton, "<Button-1>", self.check_OTP)

        self.email = Entry(
            self, 
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font = ("12")
        )
        self.email.place(
            x=428.0,
            y=563.0,
            width=584.0,
            height=62.0
        )

        self.canvas.create_text(
            428.0,
            512.0,
            anchor="nw",
            text="Email",
            fill="#FFFFFF",
            font=("Kalam Bold", 32 * -1)
        )

        self.canvas.create_text(
            313.0,
            389.0,
            anchor="nw",
            text="Enter your Email to recieve an OTP to reset your password",
            fill="#72E1F9",
            font=("Kalam Bold", 32 * -1)
        )

        self.canvas.create_text(
            398.0,
            287.0,
            anchor="nw",
            text="Forgot Your Password?",
            fill="#FFFFFF",
            font=("Kalam Bold", 64 * -1)
        )

    def check_OTP(self, event):
        OTP = rand_pass(8, self.email.get())
        #otpwin=Tk()
        #otpwin.geometry("700x300")

        print(OTP)
        self.entrOtp = askstring('OTP', 'Enter the OTP sent to your email')
        print(self.entrOtp)
        if self.entrOtp == OTP:
            showinfo('OTP', 'OTP verified successfully')
            username = getUserfromMail(self.email.get())
            self.open_createpass_window(username)
        else:
            showinfo('OTP', 'Incorrect OTP')

    def open_createpass_window(self, username):
        createpass = createpass_window(self, username, self.email.get())
        createpass.show()
        self.hide()
    
    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

