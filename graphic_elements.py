# graphic_elements.py
# Written By: Braden Carlson
# May 2025
# 
# Defines the LinkNotebook, LinkTab, and TextTab classes, which are the building
# blocks of the Link Application. 
#
# The LinkNotebook class is a ttk.Notebook with some added methods for ease of
# use in the main.py file.  Most notably, there is an addTab method which adds a
# tab to the notebook. The method declaration takes the form
#   def addTab(self, **kwargs)
# so all args passed to this method must be named by a keyword, a description of
# which can be found above the method itself. In this file, all keywords marked
# with a '*' are required to be used for the method to function correctly. 
#
# The LinkTab class is a Frame to be used as the tabs of the LinkNotebook. This
# is automatically created by the LinkNotebook.addTab method, so these do not
# need to be created in the main.py file or elsewhere. This classes' constructor
# has some keyword arguments which can be specified, which are described in the
# class definition. Each LinkTab has a menu across the top of it, which can be
# customized at construction. 
#
# The TextTab class is an extension of the LinkTab class, and is a LinkTab which
# contains a Text object to be used to view and modify files. The constructor
# for this class has some keyword arguments, which are described in the class
# definition. 

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

    # Adds a tab to the notebook. Currently the accepted keywords are 
    # * kind -  what kind of tab this will be, the accepted values for this are 
    #           currently "TextTab"
    #   text -  the text label which will appear on the tab. 
    def addTab(self, **kwargs):
        try:
            if kwargs['kind'] == "TextTab":
                newTab = TextTab(self,**kwargs)
                try:
                    self.add(newTab, text=kwargs['text'])
                except KeyError:
                    self.add(newTab, "New Tab")
        except KeyError as e:
           fatal(e) 

class LinkTab(Frame):
    # Constructor for LinkTab. Currently the accepted keywords are 
    #   menu -  The menu dictionary to use at the top of this tab
    def __init__(self,master,**kwargs):
        super().__init__(master)

        self.grid_columnconfigure(0,weight=1)
        
        # define default menu dictionary for the top of the frame
        default_menu_dict = {"File": {"New": partial(log,f"New clicked {self}"), 
                              "Open": partial(log, "Open clicked")},
                     "Edit": {"Copy": partial(log, "Copy clicked"),
                              "Paste": partial(log,"Paste clicked")}};
        try:
            menu = self.createMenubar(kwargs['menu'])
        except KeyError:
            menu = self.createMenubar(default_menu_dict)

        menu.grid(row=0, column=0,sticky="ew")

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
            submenu.grid(row=0, column=pos,sticky="EW")
            pos = pos + 1
        return menu

class TextTab(LinkTab):
    # Constructor for TextTab, see constructor for LinkTab for keywords
    # pertaining to the Tab structure. Keywords specific to the TextTab are:
    #   textwidth - width of the text box. Default is "100". 
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.filename = StringVar()
        self.filename.set("New File")

        # start counting rows at 1, since the menu is at row 0
        self.row_counter = 1

        self.createFilenameLabel()

        try:
            self.createFileArea(kwargs['textwidth'])
        except KeyError: 
            self.createFileArea()
        super().grid_rowconfigure(self.row_counter - 1, weight=1)

    # Creates an area where text can be displayed.  Returns both a reference to the
    # frame in which the text box is placed, as well as the text box itself, so that
    # the content of the text box can be updated from outside this function.
    def createFileArea(self, width="100"):
        txt = Text(self)
        txt.grid(row=self.row_counter,column=0,sticky="NSEW")
        self.row_counter = self.row_counter + 1

    def createFilenameLabel(self):
        lbl = ttk.Label(self, textvariable=self.filename)
        lbl.grid(row=self.row_counter,column=0,sticky="W")
        self.row_counter = self.row_counter + 1

def createMessageArea(master):
    frm = Frame(master)
    txt = ttk.Label(frm)
    txt.grid(row=0, column=0, sticky="E")
    return [frm,txt]

def createTab(master,tabtype="text"):
    frm = Frame(master)
    [file_frame, text_box] = createFileArea(frm)
    file_frame.grid(row=0,column=0)

