import logging
from tkinter import scrolledtext
from tkinter import *

class ScrolledTextHandler(logging.Handler):
    def __init__(self, master, width, height):
        super().__init__()
        self.scrolled_text = scrolledtext.ScrolledText(master, width=width, height=height)
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='black')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        self.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

    def place_widget(self, **kw):
        self.scrolled_text.grid(kw)
