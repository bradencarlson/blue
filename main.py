from tkinter import *
from tkinter import ttk
from functools import partial
from graphic_elements import *
import logging

class Link(ttk.Frame):


    def __init__(self, master):
        super().__init__(master)

        notebook = LinkNotebook(self)
        notebook.addTab(kind="TextTab", text="Recommended")
        notebook.addTab(kind="TextTab", text="Accepted")
        notebook.addTab(kind="TextTab", text="Master File")
        notebook.addTab(kind="OperationTab", text="Operations")
        notebook.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True)

        
        
            
root = Tk()
app = Link(root)
root.mainloop()
