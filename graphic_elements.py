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
from tkinter import filedialog, messagebox
from functools import partial
from logging import log
import colors as color
import re

class LinkNotebook(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        self.style()

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
            elif kwargs['kind'] == "OperationTab":
                newTab = OperationTab(self,**kwargs)
                try:
                    self.add(newTab, text=kwargs['text'])
                except KeyError:
                    self.add(newTab, "New Tab")
        except KeyError as e:
           fatal(e) 
    def style(self):
        S = ttk.Style()
        S.map("TNotebook.Tab",
                    background=[('selected', color.bg)],
                    foreground=[('selected', color.fg)])
        S.configure("TNotebook.Tab",
                    background=color.bg_inactive,
                    foreground=color.fg_inactive,
                    padding=[10,5])
        S.configure("TFrame", 
                    background=color.bg,
                    foreground=color.fg,
                    borderwidth=0,
                    relief="flat")
        S.configure("TLabel",
                    background=color.bg,
                    foreground=color.fg,
                    padding=[10,5])

# Since the default_menu_dict contains functions that are not defined in this
# class, but a child class, these should not be initiated directly. 
class LinkTab(ttk.Frame):
    menu_style = {
            'bg': color.bg, 
            'fg': color.fg,
            'activebackground': color.bg_active,
            'activeforeground': color.fg_active,
            'bd': 0}
    # Constructor for LinkTab. Currently the accepted keywords are 
    #   menu -  The menu dictionary to use at the top of this tab
    def __init__(self,master,**kwargs):
        super().__init__(master)

        self.grid_columnconfigure(0,weight=1)
        
        try:
            menu = self.createMenubar(kwargs['menu'])
        except KeyError:
            # define default menu dictionary for the top of the frame, 
            # which does nothing but log stuff. 
            default_menu_dict = {"File": {"New": log('New clicked'), 
                                  "Open": log('Open clicked.')},
                         "Edit": {"Copy": log("Copy clicked"),
                                  "Paste": log("Paste clicked")
                                  }}
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
        menu = ttk.Frame(self);
        pos = 0
        for (text, submenu_dict) in menu_dict.items():
            submenu = Menubutton(menu,text=text,**self.menu_style);
            menuitems = Menu(submenu, tearoff=0,**self.menu_style)
            for (submenu_label,submenu_command) in submenu_dict.items():
                menuitems.add_command(label=str(submenu_label),
                                    command=submenu_command)
            submenu.config(menu=menuitems)
            submenu.grid(row=0, column=pos,sticky="EW")
            pos = pos + 1
        return menu

    # Opens a file for editing, if there is any error in opening the file, a
    # dialog is opened and the user is asked to select a file for opening. 
    def open_file(self, filename, permissions="r"):
        f_handle = 0;
        while not f_handle:
            try:
                f_handle = open(filename,permissions)
            except Exception as e: 
                log(f"{e}")
                log("Asking user to select a file.")
                filename = filedialog.askopenfilename()
                # if the user selects cancel do nothing
                if filename == '':
                    return ''
        return f_handle



class TextTab(LinkTab):
    text_style = {
            'bg': color.bg_text,
            'fg': color.fg_text,
            'bd': 0,
            'insertbackground': color.text_insert,
            'font': "Ariel 12"}
    # Constructor for TextTab, see constructor for LinkTab for keywords
    # pertaining to the Tab structure. Keywords specific to the TextTab are:
    #   textwidth - width of the text box. Default is "100". 
    def __init__(self, master, **kwargs):

        # define the default menu for the TextTab
        default_menu_dict = {"File": {"New": self.new_file, 
                              "Open": partial(self.open_file,"NONE", "r+"),
                              "Save": self.save_file},
                     "Edit": {"Copy": partial(log, "Copy clicked"),
                              "Paste": partial(log,"Paste clicked"),
                              "Capitalize": self.capitalize_names,
                              "Sort": self.sort,
                              "Undo": self.undo,
                              "Redo": self.redo }}

        super().__init__(master, **kwargs, menu=default_menu_dict)

        self.filename_label = StringVar()
        self.filename_label.set("New File")
        self.filename = StringVar()
        self.textarea = None

        # start counting rows at 1, since the menu (placed by
        # super().__init__() ) is at row 0.
        self.row_counter = 1

        self.createFilenameLabel()

        try:
            self.textarea = self.createFileArea(kwargs['textwidth'])
        except KeyError: 
            self.textarea = self.createFileArea()
        super().grid_rowconfigure(self.row_counter - 1, weight=1)

    # Creates an area where text can be displayed.  Returns both a reference to the
    # frame in which the text box is placed, as well as the text box itself, so that
    # the content of the text box can be updated from outside this function.
    def createFileArea(self, width="100"):
        txt = Text(self, undo=True, **self.text_style)
        txt.grid(row=self.row_counter,column=0,sticky="NSEW",padx=5,pady=2)
        self.row_counter = self.row_counter + 1

        # Bind this textbox to the <<Modified>> event, which will call the 
        # on_modified method, so that a * is added to the filename label.
        txt.bind("<<Modified>>", self.on_modified)
        return txt

    # Creates a label which will contain the current value of the filename_label
    # variable. This will be used to remind the user which file is open, as well
    # as notify them when there are unsaved changes. 
    def createFilenameLabel(self):
        lbl = ttk.Label(self, textvariable=self.filename_label)
        lbl.grid(row=self.row_counter,column=0,sticky="W")
        self.row_counter = self.row_counter + 1

    # Opens a file in the TextTab's textarea. The way this is done is by passing
    # the actual open operation to the parent, then simply loading the text into
    # the textbox is the user made a choice of which file to open.  If the user
    # did not choose a file (i.e. they pressed the cancel button) this method
    # returns nothing and stops. 
    def open_file(self, filename, permissions="r"):
        f_handle = super().open_file(filename, permissions)
        if f_handle == '':
            return
        self.textarea.delete(1.0,"end")
        self.textarea.insert(1.0, f_handle.read())
        self.textarea.index(1.0)

        # Set the filename_label variable. 
        temp_filename = f_handle.name
        # TODO: This assumes unix style path names and is thus not very
        # portable.  
        temp_filename = re.sub(r"(.*)/([^/]*)$",r'\2', temp_filename)
        self.filename_label.set(temp_filename)

        # Set the current filename to be the full path of the file
        self.filename.set(f_handle.name)

        # Since we just opened a new file, make sure that the edit_modified flag
        # is turned off so there is no * next to the file name. 
        self.textarea.edit_modified(False)


    # Method to call when the textbox on this tab is modified. It simply takes
    # the curent filename_label and adds a * to the end, if there is not one
    # already. 
    def on_modified(self, event):
        if self.textarea.edit_modified():
            if not self.filename_label.get().endswith("*"):
                self.filename_label.set(self.filename_label.get() + "*")

    # Saves the file.  This is as simple as using the current filename (from
    # open_file) and writing the text from the textarea to it. 
    def save_file(self):
        if self.filename.get() == '':
            self.filename.set(filedialog.asksaveasfilename())
            self.filename_label.set(re.sub(r"(.*)/([^/]*)$",r'\2',self.filename.get()))
        try:
            f_handle = open(self.filename.get(), "w")
        except Exception as e: 
            log(f"Something went wrong trying to save {self.filename}")
            log(e)
            return
        self.textarea.edit_modified(False)
        self.filename_label.set(re.sub(r"(.*)\*$",r"\1",self.filename_label.get()))
        f_handle.write(self.textarea.get(1.0, "end-1c"))

    # If there are unsaved changes, save them, then clear the textarea and reset
    # the filename label so the user can start a new file. 
    def new_file(self):
        if self.textarea.edit_modified():
            self.save_file()
        self.textarea.delete(1.0,"end")
        self.filename.set('')
        self.textarea.edit_modified(False)
        self.filename_label.set("New File")
        return

    # Capitalize each word of the current file. Send a warning to the user first
    # confirming that this is what they want to do. 
    def capitalize_names(self):
        msg = """This operation will capitalize all words in the current file. 
        It is recommended to be used on files whose entire contents are lists of names"""
        if not messagebox.askyesno("Are you sure?", msg):
            return
        
        # mark this point as a point the user can jump back to with the Undo
        # button
        self.textarea.edit_separator()

        content = self.textarea.get(1.0,"end")
        content = re.sub(r"([a-zA-Z]+)",lambda m: m.group(0).capitalize(),content)
        self.textarea.replace(1.0,"end",content)

    # Sort lines of the textbox
    def sort(self):

        # mark this point as a point the user can jump back to with the Undo
        # button
        self.textarea.edit_separator()

        content = self.textarea.get(1.0,"end").splitlines()
        content.sort()
        content = [x for x in content if x != '']
        self.textarea.replace(1.0,"end","\n".join(content))

    # Use the undo feature from the textbox. 
    def undo(self):
        self.textarea.edit_undo()

    # Use the redo feature from the textbox. 
    def redo(self):
        self.textarea.edit_redo()



class OperationTab(LinkTab):
    def __init__(self,master, **kwargs):

        # Define the menu for the operations tab. 
        ops_menu = {'Comparison': {
            'close': exit}}
        super().__init__(master,**kwargs,menu=ops_menu)

    # This should take the output of what ever command has been run and save it
    # to a file.
    def save_file(self):
        return

