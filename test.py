#!/bin/python3

from tkinter import *
from main import Link

root = Tk()
app = Link(root)
app.addTab(kind="OperationTab", label="Ops")


app.mainloop()
