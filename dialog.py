from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import Dialog

class NewTabDialog(Dialog):
    def __init__(self,master):
        super().__init__(master)
        self.box = None
        self.tabtitle = None

    def body(self, master):
        frm = ttk.Frame(self)
        lbl = ttk.Label(frm,text="Please enter a name for the new tab, along with what kind of tab it should be.", 
                        width=50, 
                        wrap=1,
                        wraplength=350)

        self.tablabel = Entry(frm, width=32)
        self.tablabel.insert(0, "New Tab")
        self.box = ttk.Combobox(frm, values=['Text Tab', 'Operations Tab'],
                                width=30)
        self.box.set('Text Tab')



        lbl.grid(row=0, column=0)
        self.tablabel.grid(row=1,column=0, pady=5)

        self.box.grid(row=2,column=0, pady=5)

        button_frame = ttk.Frame(frm)
        ok_btn = ttk.Button(button_frame,text="Ok", command=self.ok)
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        ok_btn.pack(side="left", padx=5, pady=5)
        cancel_btn.pack(side="left", padx=5, pady=5)
        button_frame.grid(row=3, column=0)

        frm.pack()
        return frm

    def ok(self, event=None):
        newtab_label = self.tablabel.get()
        newtab_type = self.box.get()

    def cancal(self,event=None):
        return

    # Remove the default buttons
    def buttonbox(self):
        return

