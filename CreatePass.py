from tkinter import HORIZONTAL, IntVar, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Frame, filedialog, \
    messagebox, Scale
from PIL import ImageTk, Image
from pathlib import Path
from feature_extraction import *
import hashlib
import aes256encrypt as aes256
from RegisterSuccess import registersuccess_window
from vkdatabaseconnect import addUser, saveImg, addPass

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class createpass_window(Toplevel):
    def __init__(self, parent, uid, username):
        self.username = username
        self.uid = uid
        self.buttons = []
        self.num = IntVar()
        self.name = []
        super().__init__(parent)
        self.title("Generate Password")
        self.geometry("1417x878")
        self.configure(bg="#0C464A")

        self.canvas = Canvas(
            self,
            bg="#0D474B",
            height=878,
            width=1417,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        img = Image.open(relative_to_assets("bg-img1.png"))
        self.background_image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_image)

        self.canvas.place(x=0, y=0)

        self.RegisterImg = ImageTk.PhotoImage(Image.open(relative_to_assets("upload_images.png")))
        RegisterImgbutton = self.canvas.create_image(1157, 760, image=self.RegisterImg)
        self.canvas.tag_bind(RegisterImgbutton, "<Button-1>", self.upload_file)

        # self.upload_img = ImageTk.PhotoImage(Image.open(relative_to_assets("upload_images.png")))
        # upload_imgbutton = self.canvas.create_image(1151, 340, image=self.upload_img)
        # self.canvas.tag_bind(upload_imgbutton, "<Button-1>", self.upload_file)

        self.canvas.create_text(
            1055.0,
            28.0,
            anchor="nw",
            text="Create Password",
            fill="#FFFFFF",
            font=("Kalam", 48 * -1)
        )

        self.canvas.create_text(
            945.0,
            240.0,
            anchor="nw",
            text="Please set the number of images \n\t used as your password (default is 3)",
            fill="#F01B1B",
            font=("Kalam Bold", 20 * -1)
        )

        self.sliderframe = Frame(self.canvas, bg="#151E38", width=784, height=790)
        # Add the frame to the self.canvas
        self.canvas.create_window(934.0, 152.0, window=self.sliderframe, anchor="nw")

        image_label = Scale(self.sliderframe, from_=3, to=9, orient=HORIZONTAL, length=400, showvalue=0, tickinterval=1,
                            resolution=1, variable=self.num)
        image_label.pack(side="top", fill="x", padx=10, pady=10)

        # Create a frame
        self.imgframe = Frame(self.canvas, bg="#151E38", width=784, height=790)
        # Add the frame to the self.canvas
        self.canvas.create_window(52.0, 50.0, window=self.imgframe, anchor="nw")

    def show_img(self, imgnm):
        self.name.append(imgnm)
        if len(self.name) == self.num.get():
            for i in range(len(self.buttons)):
                self.buttons[i].config(state="disabled")
            self.generate_desci(self.name)

    def upload_file(self, event):
        f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'),
                   ('PNG Files', '*.png')]  # type of files to select
        filename = filedialog.askopenfilename(multiple=True, filetypes=f_types)
        imgs = saveImg(filename, self.uid)
        print("Done")

        col = 1  # start from column 1
        row = 5  # start from row 3
        for f in imgs:
            pil_image = Image.fromarray(f)
            img = pil_image.resize((100, 100))  # new width & height
            img = ImageTk.PhotoImage(img)
            btn = Button(self.imgframe, command=lambda imgf=f: self.show_img(imgf))
            btn.image = img
            btn['image'] = img
            btn.grid(row=row, column=col)
            self.buttons.append(btn)
            if col == 5:  # start new line after third column
                row = row + 1  # start with next row
                col = 1  # start with first column
            else:  # within the same row
                col = col + 1  # increase to next column

    def generate_desci(self, filename):
        test = []
        for f in filename:
            # load and prepare the photograph
            photo = extract_features(f)
            # generate description
            max_length = 33
            description = generate_desc(model, tokenizer, photo, max_length)
            test.append(clean_description(description))
        enc_it = " ".join(test)
        print(enc_it)
        hashed_string = hashlib.sha256(enc_it.encode('utf-8')).hexdigest()
        passwd = aes256.encrypt(hashed_string, self.username)
        addPass(self.uid, passwd)
        self.open_success_window()

    def open_success_window(self):
        regsuccess = registersuccess_window(self)
        regsuccess.show()
        self.hide()

    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()
