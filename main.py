import Database_GUI
from tkinter import *

if __name__ == '__main__':
    root = Tk()
    root.geometry("490x400")
    root.resizable(0, 0)
    gui = Database_GUI.Database_GUI(root)
    root.mainloop()

# urmatorul pas este sa faci cumva ca atunci cand faci o fereastra noua cea de log in sa discpara si cand iesi din aia
# sa apara din nou, dupa faci schemele pentru fiecare dintre funcionalitatile ferestrelor
