import tkinter as tk
from tkinterdnd2 import TkinterDnD
from gui.main_gui import CLISelector

def main():
    root = TkinterDnD.Tk()
    app = CLISelector(root)
    root.minsize(550, 400)
    root.mainloop()

if __name__ == "__main__":
    main()