import Database_GUI
from tkinter import *
from Database_functions import *

if __name__ == '__main__':
    connect()
    initialize_database()
    root = Tk()
    root.geometry("490x400")
    root.resizable(0, 0)
    gui = Database_GUI.Database_GUI(root)
    root.mainloop()

