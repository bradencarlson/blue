from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import Dialog

class NewTabDialog(Dialog):
    def __init__(self,master):
        super().__init__(master)

    def body(self, master):
        frm = ttk.Frame(self)
        btn = ttk.Button(frm, text="hello from custom dialog")
        btn.pack()
        frm.pack()
        return frm




