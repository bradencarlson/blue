from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import Dialog, Toplevel, _place_window
import logging as log

class NewTabDialog(Dialog):
    def __init__(self,master,title=None):

        ##################################################
        ### This was modified from the simpledialog.py, found at 
        ### https://github.com/python/cpython/blob/3.13/Lib/tkinter/simpledialog.py
        if master is None:
            log.fatal("Master cannot be None in __init__ for NewTabDialog")
            
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
        self.error_lbl
        return self.apply()

    def body(self, master):
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
        button_frame = ttk.Frame(self)
        ok_btn = ttk.Button(button_frame,text="Ok", command=self.ok)
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        ok_btn.pack(side="left", padx=5, pady=5)
        cancel_btn.pack(side="left", padx=5, pady=5)
        button_frame.pack(fill="both",expand=True,padx=0,pady=0)
        return

def ask_new_tab(master):
    d = NewTabDialog(master)
    return [d.tablabel_result, d.tabkind]

