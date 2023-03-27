from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Frame
from PIL import ImageTk,Image
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class registersuccess_window(Toplevel):
    def __init__(self, parent):
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

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            708.0,
            320.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            449.0,
            439.0,
            anchor="nw",
            text="Successfully Registered...!",
            fill="#FFFFFF",
            font=("Kalam", 48 * -1)
        )
    
    def hide(self):
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

if __name__ == "__main__":
    window = Tk()
    main_window = registersuccess_window(window)
    window.mainloop()