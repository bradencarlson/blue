from tkinter import *
from tkinter import ttk
from functools import partial
from graphic_elements import *

class Link(ttk.Frame):


    def __init__(self, master):
        super().__init__(master)

        notebook = LinkNotebook(self)
        notebook.addTab(kind="TextTab", text="Recommended")
        notebook.addTab(kind="TextTab", text="Accepted")
        notebook.addTab(kind="TextTab", text="Master File")
        notebook.addTab(kind="OperationTab", text="Operations")
        notebook.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True)

        


    def save_file(self, textbox = None):
        if textbox==None:
            return

        filename = self.current_filename
        try: 
            f_handle = open(filename, "w")
        except:
            self.log(f"Something went wrong opening {filename}\n Asking for another file...")
            filename = filedialog.asksaveasfilename()
            try:
                f_handle = open(filename,"w")
            except: 
                self.log("Something still went wrong with new filename\n Aborting...")
                return

        try:
            f_handle.write(textbox.get(1.0,END));
        except:
            self.log("Something went wrong writing to file.")
            return
        self.sendMessage("Save successful.")


    def log(self, msg):
        print(msg)

        
    def sendMessage(self, msg):
        self.message_textbox.config(text=msg)
            
root = Tk()
app = Link(root)
root.mainloop()
