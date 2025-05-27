from tkinter import *
from tkinter import ttk

# Creates the menubar which sits at the top of the screen. 
def createMenubar(master):
    menu = Menu(master);
    file = Menu(menu, tearoff=0)
    file.add_command(label="Open", command = None)
    file.add_command(label="New", command = None)
    menu.add_cascade(label="File", menu = file)
    master.config(menu = menu)

# Creates a frame which holds the logo for the application. This 
# is meant to be used as the first row of the main application. 
def createLogo(master):
    frm = Frame(master)

    # Add a label in the top left of this frame. 
    lbl = ttk.Label(frm, padding=10, text="Welcome", foreground="Red",
                    font="Monospace 17", justify="left")
    lbl.grid(row=0,column=0,sticky="E");

    return frm

# Creates an area where text can be displayed.  Returns both a reference to the
# frame in which the text box is placed, as well as the text box itself, so that
# the content of the text box can be updated from outside this function.
def createFileArea(master):
    frm = Frame(master)

    txt = Text(frm, width="40")
    txt.grid(row=0,column=0)
    return [frm, txt]
