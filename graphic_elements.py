from tkinter import *
from tkinter import ttk

# Creates the menubar which sits at the top of the screen. The menu dictionary
# which is passed to this method should have a top level menu item as the key,
# then a dictionary as the value, the keys of which are labels, and values
# commands to be run. For example: 
# 
# to generate the menu 
# File
#   New -> new_function
#   Open -> open_function
#
# the following should be passed:
#
# {"File": {"New": new_function, "Open": open_function}}
#
def createMenubar(master, menu_dict):
    menu = Menu(master);
    for (text, submenu_dict) in menu_dict.items():
        submenu = Menu(menu,tearoff=0);
        for (submenu_label,submenu_command) in submenu_dict.items():
            submenu.add_command(label=str(submenu_label),
                                command=submenu_command)
        menu.add_cascade(label=str(text), menu = submenu)
    master.config(menu=menu)

# Creates a frame which holds the logo for the application. This 
# is meant to be used as the first row of the main application. 
def createLogo(master):
    frm = Frame(master)

    # Add a label in the top left of this frame. 
    lbl = ttk.Label(frm, padding=10, text="Welcome", foreground="Red",
                    font="Monospace 17", justify="left")
    lbl.grid(row=0,column=0);

    return frm

# Creates an area where text can be displayed.  Returns both a reference to the
# frame in which the text box is placed, as well as the text box itself, so that
# the content of the text box can be updated from outside this function.
def createFileArea(master):
    frm = Frame(master)

    txt = Text(frm, width="40")
    txt.grid(row=0,column=0)
    return [frm, txt]

def createMessageArea(master):
    frm = Frame(master)
    txt = ttk.Label(frm)
    txt.grid(row=0, column=0, sticky="E")
    return [frm,txt]

def createTab(master,tabtype="text"):
    frm = Frame(master)
    [file_frame, text_box] = createFileArea(frm)
    file_frame.grid(row=0,column=0)

