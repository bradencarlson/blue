""" dialog.py
Author: Braden Carlson <bradenjcarlson@live.com>

Provides the dialogs NewTabDialog, CutDialog, and ErrorDialog. These are used to
display and recieve data to and from the user when performing actions that need
information.  """

from tkinter import Frame, Entry
from tkinter import ttk
from tkinter import _get_temp_root
from tkinter.simpledialog import Dialog, Toplevel, _place_window
import re as regex
import sys

class NewTabDialog(Dialog):
    """ A Dialog which prompts the user for details when adding a new tab to the
    application.  Asks the user to enter a name for the tab, as well as what
    kind of tab it should be. """

    def __init__(self,master,title=None):
        """ Initialize the NewTabDialog. """

        ##################################################
        ### This was modified from the simpledialog.py, found at
        ### https://github.com/python/cpython/blob/3.13/Lib/tkinter/simpledialog.py
        if master is None:
            fatal("Master cannot be None in __init__ for NewTabDialog")

        Toplevel.__init__(self, master)

        self.withdraw() # remain invisible for now
        # If the parent is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if master is not None and master.winfo_viewable():
            self.transient(master)

        if title:
            self.title(title)

        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style",
                  self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes(type="dialog")

        self.parent = master

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        # Basically the reason for including all of this was to set these two
        # values to 0.
        body.pack(padx=0, pady=0)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        _place_window(self, master)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)


        ### End content from simpledialog.py
        ##################################################

        self.box = None
        self.tabtitle = None
        self.error_lbl = None
        self.tablabel_result = None
        self.tabkind = None
        return self.apply()

    def body(self, master):
        """ Creates the body of the Dialog, which allows the user to enter a
        name for the new tab, as well as what kind it will be. """

        frm = ttk.Frame(master)
        lbl = ttk.Label(frm,text="Please enter a name for the new tab, along with what kind of tab it should be.",
                        width=50,
                        wrap=1,
                        wraplength=350)

        self.error_lbl = ttk.Label(frm, text="Something went wrong, please try again",
                              foreground="red",
                              width=50)

        self.tablabel = Entry(frm, width=32)
        self.tablabel.insert(0, "New Tab")
        self.box = ttk.Combobox(frm, values=['Text Tab', 'Operations Tab'],
                                width=30)
        self.box.set('Text Tab')

        lbl.pack()
        self.tablabel.pack(pady=5)
        self.box.pack(pady=5)

        frm.pack(expand=True)

        return frm

    def validate(self):
        """ Makes sure that the data that the user entered is valid. This is
        very probable, but there is the possibility that the user enters
        something into the Combobox instead of selecting one of the options. """

        self.tablabel_result = self.tablabel.get()
        kind = self.box.get()
        if kind == "Text Tab":
            self.tabkind = "TextTab"
        elif kind == "Operations Tab":
            self.tabkind = "OperationTab"
        else:
            self.tabkind = ""
            self.error_lbl.pack()
            return 0
        return 1


    # Remove the default buttons
    def buttonbox(self):
        """ Create the buttons for this dialog, just an ok button as well as a
        cancel button. """

        button_frame = ttk.Frame(self)
        ok_btn = ttk.Button(button_frame,text="Ok", command=self.ok)
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        ok_btn.pack(side="left", padx=5, pady=5)
        cancel_btn.pack(side="left", padx=5, pady=5)
        button_frame.pack(fill="both",expand=True,padx=0,pady=0)

def ask_new_tab(master):
    """ Creates a NewTabDialog and returns the tablabel and the type that the
    user enters and selects. """

    d = NewTabDialog(master)
    return [d.tablabel_result, d.tabkind]

class CutDialog(Dialog):
    """ Dialog to prompt the user for a cut range, to be used to filter columns
    out of their data. """

    def __init__(self, master, title=None):
        """ This method was mostly copied from the simpledialog.py module, see
        below. """

        ##################################################
        ### This was modified from the simpledialog.py, found at
        ### https://github.com/python/cpython/blob/3.13/Lib/tkinter/simpledialog.py
        if master is None:
            fatal("Master cannot be None in __init__ for CutDialog")

        Toplevel.__init__(self, master)

        self.withdraw() # remain invisible for now
        # If the parent is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if master is not None and master.winfo_viewable():
            self.transient(master)

        if title:
            self.title(title)

        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style",
                  self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes(type="dialog")

        self.parent = master

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        # Basically the reason for including all of this was to set these two
        # values to 0.
        body.pack(padx=0, pady=0)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        _place_window(self, master)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)


        ### End content from simpledialog.py
        ##################################################

        self.rng_entry = None
        self.rng = None
        return self.apply()

    def body(self, master):
        """ Create the main body of the dialog, namely a label with
        instructions, and and entry field for the user to provide a range. """

        frm = ttk.Frame(master)

        inst = ttk.Label(frm, text="Please enter a range of numbers (separated by commas \
if necessary, i.e. 1-4,7-10) indicating which columns of data to KEEP.",
                        width=50,
                        wrap=1,
                        wraplength=350)
        inst.pack()

        self.rng_entry = Entry(frm)
        self.rng_entry.pack()

        # Do not pack this here, this will be packed by the validate() method if
        # the provided range does not match the regex ^[0-9,-]+$
        self.err_msg = ttk.Label(frm, text="Something went wrong, please try again.",
                        foreground="red",
                        width=50,
                        wrap=1,
                        wraplength=350)

        frm.pack(expand=True)

        return frm

    def buttonbox(self):
        """ Override the default buttonbox, so that the style matches the style
        of the rest of the application. """

        frm = ttk.Frame(self)
        ok_button = ttk.Button(frm, text="Ok", command=self.ok)
        ok_button.pack(side="left",padx=5,pady=5)
        cancel_button = ttk.Button(frm, text="Cancel", command=self.cancel)
        cancel_button.pack(side="left",padx=5,pady=5)
        frm.pack(side="bottom", fill="both", expand=True,padx=0, pady=0)

    def validate(self):
        """ If the provided range matches the regex ^[0-9,-]+$, then continue,
        otherwise show the error message. """

        self.rng = self.rng_entry.get()
        if regex.match(r'^[0-9,-]+$', self.rng) is None:
            self.err_msg.pack()
            return 0
        return 1

def ask_num_range(master):
    """ Convenience method to create a CutDialog and get it's range. """

    d = CutDialog(master)
    try:
        return d.rng
    except AttributeError:
        return [-1]


class ErrorDialog(Dialog):
    """ Displays an error to the user. Only the action 'OK' is provided, which
    closes the dialog. """

    def __init__(self,master,title=None,msg="Error!"):
        """ Initializes the ErrorDialog. """

        self.error_message = msg

        ##################################################
        ### This was modified from the simpledialog.py, found at
        ### https://github.com/python/cpython/blob/3.13/Lib/tkinter/simpledialog.py
        if master is None:
            master = _get_temp_root()

        Toplevel.__init__(self, master)

        self.withdraw() # remain invisible for now
        # If the parent is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if master is not None and master.winfo_viewable():
            self.transient(master)

        if title:
            self.title(title)

        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style",
                  self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes(type="dialog")

        self.parent = master

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        # Basically the reason for including all of this was to set these two
        # values to 0.
        body.pack(padx=0, pady=0)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        _place_window(self, master)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)


        ### End content from simpledialog.py
        ##################################################

    def body(self, master):
        """ Creates a label to be used to display the message to the user. """

        frm = ttk.Frame(master)
        l = ttk.Label(frm, text=self.error_message,
                      width=50,
                      wrap=1,
                      wraplength=350)
        l.pack()
        frm.pack()
        return frm

    def buttonbox(self):
        """ Creates the buttons for this dialog, only the ok button is 
        provided.  """
        frm = ttk.Frame(self)
        ok_button = ttk.Button(frm,text="OK", command=self.cancel)
        ok_button.pack(side="right",padx=5,pady=5)
        frm.pack(side="bottom",fill="both", expand=True)

def log(msg):
    """ Log the message provided. """

    print(msg)

def fatal(msg):
    """ Log the message provided, then quit. """

    print(msg)
    sys.exit()

def error(master, msg):
    """ Covenience method to display an error to the user. Creates an
    ErrorDialog and shows it. """

    ErrorDialog(master, msg=msg)
