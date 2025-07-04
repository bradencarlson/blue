#!/bin/python3

from tkinter import *
from main import Link

root = Tk()
app = Link(root)
app.add_tab(kind="OperationTab", label="Ops")
app.add_tab(kind="TextTab", label="Text")

app.select(1)
tab = app.current_tab()

tab.open_file("caps-test.txt")

app.mainloop()

