from tkinter import Tk
from login import login_window

if __name__ == "__main__":
    window = Tk()
    window.withdraw()
    main_window = login_window(window)
    window.mainloop()
    