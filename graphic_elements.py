from tkinter import *
from tkinter import ttk
from functools import partial
from logging import log

class LinkNotebook(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)

    def getTabs(self):
        return self.tabs()

    def selectTab(self, tab_id):
        return self.tab(tab_id)

    def addTab(self, text="New Tab",menu_dict=None):
        newTab = LinkTab(self,menu_dict)
        self.add(newTab, text=text)

class LinkTab(Frame):
    def __init__(self,master,menu_dict=None):
        super().__init__(master)

        
        # define menu dictionary for the top of the window
        default_menu_dict = {"File": {"New": partial(log,f"New clicked {self}"), 
                              "Open": partial(log, "Open clicked")},
                     "Edit": {"Copy": partial(log, "Copy clicked"),
                              "Paste": partial(log,"Paste clicked")}};
        if menu_dict == None:
            menu = self.createMenubar(default_menu_dict)
        else:
            menu = self.createMenubar(menu_dict)
        menu.grid(row=0, column=0)


    # Creates the menubar which sits at the top of the current tab. The menu dictionary
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
    def createMenubar(self, menu_dict):
        menu = Frame(self);
        pos = 0
        for (text, submenu_dict) in menu_dict.items():
            submenu = Menubutton(menu,text=text);
            menuitems = Menu(submenu, tearoff=0)
            for (submenu_label,submenu_command) in submenu_dict.items():
                menuitems.add_command(label=str(submenu_label),
                                    command=submenu_command)
            submenu.config(menu=menuitems)
            submenu.grid(row=0, column=pos)
            pos = pos + 1
        return menu

class TextTab(LinkTab):
    def __init__(self, master):
        super().__init__(master)
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

