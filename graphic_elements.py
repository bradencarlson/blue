""" graphic_elements.py
Written By: Braden Carlson
May 2025

Defines the LinkNotebook, LinkTab, and TextTab classes, which are the building
blocks of the Link Application.

The LinkNotebook class is a ttk.Notebook with some added methods for ease of
use in the main.py file.  Most notably, there is an add_tab method which adds a
tab to the notebook. The method declaration takes the form
  def add_tab(self, **kwargs)
so all args passed to this method must be named by a keyword, a description of
which can be found above the method itself. In this file, all keywords marked
with a '*' are required to be used for the method to function correctly.

The LinkTab class is a Frame to be used as the tabs of the LinkNotebook. This
is automatically created by the LinkNotebook.add_tab method, so these do not
need to be created in the main.py file or elsewhere. This classes' constructor
has some keyword arguments which can be specified, which are described in the
class definition. Each LinkTab has a menu across the top of it, which can be
customized at construction.

The TextTab class is an extension of the LinkTab class, and is a LinkTab which
contains a Text object to be used to view and modify files. The constructor
for this class has some keyword arguments, which are described in the class
definition. """

from tkinter import Menu, Menubutton, StringVar, Text, LEFT
from tkinter import ttk
from tkinter import filedialog, messagebox
from functools import partial
import colors as color
import fops as fo
import dialog as dlg
import re

class LinkNotebook(ttk.Notebook):
    """ A notebook to hold tabs for the user. Currently this class has the
    add_tab method, and a style method. The style method sets the style for the
    main widgets which are used in this class and it's children.

    The add_tab method expects a few keyword arguments from the caller:
        kind - what kind of tab to add, see method for more details
        text - the label of the new tab
    """

    def __init__(self, master):
        super().__init__(master)
        self.style()

        # I don't think that there is any way to acces the content of the tabs
        # in the ttk.Notebook class, so let's keep track of a list of the Tabs,
        # as well as a list to keep track of their labels. 
        self.tab_list = []
        self.tab_labels = []

    def add_tab(self, **kwargs):
        """ Adds a tab to the notebook. A star indicates a required parameter. 
        Currently the accepted keywords are
          * kind -  what kind of tab this will be, the accepted values for this are
                  currently "TextTab"
            text -  the text label which will appear on the tab. """

        try:
            if kwargs['kind'] == "TextTab":
                new_tab = TextTab(self,**kwargs)
                try:
                    self.add(new_tab, text=kwargs['text'])
                    self.tab_labels.append(kwargs['text'])
                except KeyError:
                    label = f"Tab {len(self.tab_list)}"
                    self.add(new_tab, label)
                    self.tab_labels.append(label)

                # Add this tab to the tab_list
                self.tab_list.append(new_tab)
            elif kwargs['kind'] == "OperationTab":
                new_tab = OperationTab(self,**kwargs)
                try:
                    self.add(new_tab, text=kwargs['text'])
                    self.tab_labels.append(kwargs['text'])
                except KeyError:
                    label = f"Tab {len(self.tab_list)}"
                    self.add(new_tab, label)
                    self.tab_labels.append(label)

                # Add this tab to the tab_list
                self.tab_list.append(new_tab)
        except KeyError as e:
            fatal(e)

    def get_tab(self, index):
        """ Return the LinkTab object at index, or None if index is out of
        bounds. """

        try: 
            return self.tab_list[index]
        except IndexError:
            return None

    def get_filenames(self):
        """ Returns a list of all the TextTabs which are contained in this
        notebook.  This is used in the OperationTab class to allow the user to
        select files for diffing. """

        tabs = [tab.filename.get() for tab in self.tab_list if isinstance(tab, TextTab) ]
        return tabs

    def get_text_tab_labels(self):
        """ Returns a list of TextTab labels """

        labels = []
        for i in range(0,len(self.tab_list)):
            if isinstance(self.tab_list[i], TextTab):
                labels.append(self.tab_labels[i])
        return labels

    def style(self):
        """ Sets the style for most of the widgets that this class and it's
        children use. This provides a uniform look across the application."""

        s = ttk.Style()
        s.map("TNotebook.Tab",
                    background=[('selected', color.bg)],
                    foreground=[('selected', color.fg)])
        s.configure("TNotebook.Tab",
                    background=color.bg_inactive,
                    foreground=color.fg_inactive,
                    padding=[10,5])
        s.configure("TFrame",
                    background=color.bg,
                    foreground=color.fg,
                    borderwidth=0,
                    relief="flat")
        s.configure("TLabel",
                    background=color.bg,
                    foreground=color.fg,
                    padding=[10,5])

class LinkTab(ttk.Frame):
    """ Since the default_menu_dict contains functions that are not defined in this
    class, but a child class, these should not be initiated directly. """

    def __init__(self,master,**kwargs):
        """ Constructor for LinkTab. Currently the accepted keywords are
            menu -  The menu dictionary to use at the top of this tab """

        super().__init__(master)

        self.grid_columnconfigure(0,weight=1)

        try:
            menu = self.create_menubar(kwargs['menu'])
        except KeyError:
            # define default menu dictionary for the top of the frame,
            # which does nothing but log stuff.
            default_menu_dict = {"File": {"New": dlg.log('New clicked'),
                                "Open": dlg.log('Open clicked.'),
                                "Close": self.close},
                         "Edit": {"Copy": dlg.log("Copy clicked"),
                                  "Paste": dlg.log("Paste clicked")
                                  }}
            menu = self.create_menubar(default_menu_dict)

        menu.grid(row=0, column=0,sticky="ew")


    def create_menubar(self, menu_dict):
        """ Creates the menubar which sits at the top of the current tab. The menu dictionary
        which is passed to this method should have a top level menu item as the key,
        then a dictionary as the value, the keys of which are labels, and values
        commands to be run. For example:
 
        to generate the menu
        File
          New -> new_function
          Open -> open_function
 
        the following should be passed:
 
        {"File": {"New": new_function, "Open": open_function}} """

        menu = ttk.Frame(self)
        pos = 0
        for (text, submenu_dict) in menu_dict.items():
            submenu = Menubutton(menu,text=text,**color.menu_style)
            menuitems = Menu(submenu, tearoff=0,**color.menu_style)
            for (submenu_label,submenu_command) in submenu_dict.items():
                menuitems.add_command(label=str(submenu_label),
                                    command=submenu_command)
            submenu.config(menu=menuitems)
            submenu.grid(row=0, column=pos,sticky="EW")
            pos = pos + 1
        return menu

    def open_file(self, filename, permissions="r"):
        """ Opens a file for editing, if there is any error in opening the file, a
        dialog is opened and the user is asked to select a file for opening. """

        f_handle = 0
        while not f_handle:
            try:
                f_handle = open(filename, permissions)
                return f_handle
            except FileNotFoundError as e:
                dlg.log(f"{e}")
                dlg.log("Asking user to select a file.")
                filename = filedialog.askopenfilename()
                # if the user selects cancel do nothing
                if filename == '':
                    return ''

    def close(self):
        """ Close the current tab (self) """
        index = self.master.index(self.master.select())
        self.master.forget(index)



class TextTab(LinkTab):
    """ Tab which contains a large text area for viewing files, as well as a
    menu which contains the standard things for dealing with files, along with
    some operations which are specific to this application. """

    def __init__(self, master, **kwargs):
        """ Constructor for TextTab, see constructor for LinkTab for keywords
        pertaining to the Tab structure. Keywords specific to the TextTab are:
          textwidth - width of the text box. Default is "100". """

        # define the default menu for the TextTab
        default_menu_dict = {"File": {"New": self.new_file,
                              "Open": partial(self.open_file,"NONE", "r+"),
                              "Save": self.save_file,
                              "Close": self.close},
                     "Edit": {"Copy": partial(dlg.log, "Copy clicked"),
                              "Paste": partial(dlg.log,"Paste clicked"),
                              "Capitalize": self.capitalize_names,
                              "Sort": self.sort,
                              "Undo": self.undo,
                              "Redo": self.redo, 
                              "Cut": self.cut}}

        super().__init__(master, **kwargs, menu=default_menu_dict)

        self.filename_label = StringVar()
        self.filename_label.set("New File")
        self.filename = StringVar()
        self.textarea = None

        # start counting rows at 1, since the menu (placed by
        # super().__init__() ) is at row 0.
        self.row_counter = 1

        self.create_filename_label()

        try:
            self.textarea = self.create_file_area(kwargs['textwidth'])
        except KeyError:
            self.textarea = self.create_file_area()
        super().grid_rowconfigure(self.row_counter - 1, weight=1)

    def create_file_area(self):
        """ Creates an area where text can be displayed.  Returns both a reference to the
        frame in which the text box is placed, as well as the text box itself, so that
        the content of the text box can be updated from outside this function. """

        txt = Text(self, undo=True, **color.text_style)
        txt.grid(row=self.row_counter,column=0,sticky="NSEW",padx=5,pady=2)
        self.row_counter = self.row_counter + 1

        # Bind this textbox to the <<Modified>> event, which will call the
        # on_modified method, so that a * is added to the filename label.
        txt.bind("<<Modified>>", self.on_modified)
        return txt

    def create_filename_label(self):
        """ Creates a label which will contain the current value of the filename_label
        variable. This will be used to remind the user which file is open, as well
        as notify them when there are unsaved changes. """

        lbl = ttk.Label(self, textvariable=self.filename_label)
        lbl.grid(row=self.row_counter,column=0,sticky="W")
        self.row_counter = self.row_counter + 1

    def open_file(self, filename, permissions="r"):
        """ Opens a file in the TextTab's textarea. The way this is done is by passing
        the actual open operation to the parent, then simply loading the text into
        the textbox is the user made a choice of which file to open.  If the user
        did not choose a file (i.e. they pressed the cancel button) this method
        returns nothing and stops. """

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


    def on_modified(self, event):
        """ Method to call when the textbox on this tab is modified. It simply takes
        the curent filename_label and adds a * to the end, if there is not one
        already. """

        if self.textarea.edit_modified():
            if not self.filename_label.get().endswith("*"):
                self.filename_label.set(self.filename_label.get() + "*")

    def save_file(self):
        """ Saves the file.  This is as simple as using the current filename (from
        open_file) and writing the text from the textarea to it. """

        if self.filename.get() == '':
            self.filename.set(filedialog.asksaveasfilename())
            self.filename_label.set(re.sub(r"(.*)/([^/]*)$",r'\2',self.filename.get()))
        try:
            f_handle = open(self.filename.get(), "w")
        except FileNotFoundError:
            dlg.log(f"{self.filename} was not found.")
            dlg.log(e)
            return
        except IsADirectoryError:
            dlg.log(f"{self.filename} is a directory, cannot save file.")
            return

        self.textarea.edit_modified(False)
        self.filename_label.set(re.sub(r"(.*)\*$",r"\1",self.filename_label.get()))
        f_handle.write(self.textarea.get(1.0, "end-1c"))

    def new_file(self):
        """ If there are unsaved changes, save them, then clear the textarea and reset
        the filename label so the user can start a new file. """

        if self.textarea.edit_modified():
            self.save_file()
        self.textarea.delete(1.0,"end")
        self.filename.set('')
        self.textarea.edit_modified(False)
        self.filename_label.set("New File")
        return

    def capitalize_names(self):
        """ Capitalize each word of the current file. Send a warning to the user first
        confirming that this is what they want to do. """

        msg = """This operation will capitalize all words in the current file.
        It is recommended to be used on files whose entire contents are lists of names"""
        if not messagebox.askyesno("Are you sure?", msg):
            return

        # mark this point
        self.mark_jump_point()

        content = self.get_content()
        content = fo.capitalize_words(content)
        self.replace(1.0,"end",content)

    def sort(self):
        """ Sort lines of the textbox """

        # mark this point
        self.mark_jump_point()
        s = self.get_content()
        s = fo.sort_lines(s)
        self.replace(1.0,"end-1c",s)

    def mark_jump_point(self):
        """ Make the point at which this is called a place the user can jump
        back to useing the undo and redo buttons. The command to do this wasn't
        long, but does not have a very intuitive name. """

        self.textarea.edit_separator()

    def get_lines(self):
        """ Get the content of the text area, as a list of strings, each
        of which is a line of the file. """

        return self.get_content().splitlines()

    def get_content(self):
        """ Get the content of the text area, as a single string. """

        return self.textarea.get(1.0,"end-1c")

    def undo(self):
        """ Use the undo feature from the textbox. """
        self.textarea.edit_undo()

    def redo(self):
        """ Use the redo feature from the textbox. """
        self.textarea.edit_redo()

    def replace(self, start, end, string):
        """ Call the replace method of the textarea in this tab. """
        self.mark_jump_point()
        self.textarea.delete(start,end)
        self.textarea.insert(start,string)

    def cut(self,**opts): 
        rng = None
        try: 
            rng = opts["r"]
        except KeyError:
            rng = dlg.ask_num_range(self)

        # ask_num_range returns a list with a single entry (-1) when the user
        # hits the cancel button. In this case, just stop here. 
        if rng[0] == -1:
            return 

        content = self.get_content()
        new_content = fo.cut(content,f=rng)
        self.replace(1.0,"end", new_content)



class OperationTab(LinkTab):
    """ This tab contains the controls for taking diffs of files (not line by
    line) which are contained in the other tabs of the app. """

    def __init__(self,master, **kwargs):

        # Define the menu for the operations tab.
        ops_menu = {'File': {
            'Close': self.close, 'Save As': self.save_as, 'Save': self.save_file}}
        super().__init__(master,**kwargs,menu=ops_menu)

        # for my own reference, declare what children this Tab will keep track
        # of, and what type they are.

        self.master = master
        self.tab_list = [] # list of tabs from self.master
        master.bind("<<NotebookTabChanged>>", self.update_tab_list)

        self.output = None # Text()

        self.row_counter = 1 # int (obviously)

        self.file1_select = None # ttk.Combobox
        self.file2_select = None # ttk.Combobox

        self.filename = StringVar() # String
        self.filename.set("NONE")

        # Create the layout for this tab

        self.create_output_area()
        self.create_controls()

    def update_tab_list(self,event):
        self.tab_list = self.master.get_text_tab_labels()
        # Destroy the contols frame before recreating it, this is HIGHLY
        # dependent on the order in which create_output_area and create_controls
        # are called and should eventually be changed to make sure that the
        # controls frame is really the one being removed here. 
        self.winfo_children()[2].destroy()
        self.create_controls()

    def save_as(self): 
        """ Sets the filename to be NONE so that the save_file method prompts
        the user for a new one. """

        self.filename.set('NONE')
        self.save_file()

    def save_file(self):
        """ This takes the content of the output text area and saves it to a
        file.  If the value of self.filename.get() is the string 'NONE', then it
        prompts the user to choose a file or enter a new filename. """
        
        if self.filename.get() == "NONE":
            self.filename.set(filedialog.asksaveasfilename())
        
        try: 
            with open(self.filename.get(), "w") as f_handle: 
                f_handle.write(self.output.get(1.0, "end-1c"))
        except FileExistsError: 
            log(f"{self.filename.get()} already exists, aborting.")
            self.filename.set("NONE")
        except IsADirectoryError:
            log(f"{self.filename.get()} is a directory, setting filename to NONE so the user can try again.")
            self.filename.set("NONE")

        return

    def create_output_area(self):
        """ Puts a text area in the tab so that output from the various commands
        can be viewed and saved if desired. """

        self.output = Text(self,**color.text_style)

        self.grid_rowconfigure(self.row_counter, weight=1)

        self.output.grid(row=self.row_counter, column=1, sticky="NS")

    def create_controls(self):

        frm = ttk.Frame(self)

        diff_label = ttk.Label(frm, text="Differences", width=50, anchor="w")
        diff_label.pack()

        # Create the label for the first tab
        file1_label = ttk.Label(frm,text="Choose first tab:",
                                anchor="w",width=50)
        file1_label.pack()

        # Create the Combobox for the first tab
        self.file1_select = ttk.Combobox(frm,  values=self.tab_list)

        self.file1_select.pack(pady=5)

        # Create the label for the second file
        file2_label = ttk.Label(frm, text="Choose second tab:", 
                                anchor="w", width=50)
        file2_label.pack()

        # Create the Combobox for the second file
        self.file2_select = ttk.Combobox(frm, values=self.tab_list)

        self.file2_select.pack(pady=5)

        

        buttons = {'Take Difference': self.take_difference} 
        button_box = self.create_button_box(frm, buttons,"h")
        button_box.pack(pady=5)
        frm.grid(row=self.row_counter,column=0,sticky="NS")

    def take_difference(self):
        idx1 = self.file1_select.current()
        idx2 = self.file2_select.current()

        if idx1 == -1 or idx2 == -1:
            return

        self.output.delete(1.0, "end")
        filename_one = self.master.get_filenames()[idx1]
        filename_two = self.master.get_filenames()[idx2]
        nonmatches = fo.difference(filename_one, filename_two)
        self.output.insert(1.0, '\n'.join(nonmatches))


    def create_button_box(self, master, button_dict, orientation):
        """ Creates a ttk.Frame which contains the buttons defined in the
        button_dict.  The buttons may be layed out in a row or in a column,
        which is controlled by the orientation parameter, which may be one of
        the values "vertical", "v", "horizontal", or "h". 

        Since there may be widgets which contains rows or columns of buttons,
        the master of this widget may be specified with the master parameter. """

        frm = ttk.Frame(master)
        for label, cmd in button_dict.items():
            btn = ttk.Button(frm, text=label, command=cmd)
            if orientation == "vertical" or orientation=="v":
                btn.pack(side="top",pady=2)
            elif orientation == "horizontal" or orientation == "h":
                btn.pack(side="left",padx=3)
        return frm


