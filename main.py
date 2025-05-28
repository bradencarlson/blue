from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from graphic_elements import *

class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # define menu dictionary for the top of the window
        menu_dict = {"File": {"New": partial(self.log,"New clicked"), 
                              "Open": partial(self.log, "Open clicked")}};

        createMenubar(master, menu_dict)
        frm = createLogo(master)
        [fileArea, text] = createFileArea(master)
        btn = ttk.Button(frm, text="Open File", 
                         command=partial(self.open_file, "NONE",textbox=text))
        btn.grid(row=0, column=1)
        frm.grid(row=0,column=0,sticky="W")
        fileArea.grid(row=1, column=0)

        

    def open_file(self, filename, permissions="r", textbox= None):
        if filename == "NONE":
            filename = filedialog.askopenfilename()

        try:
            f_handle = open(filename, permissions)
            if textbox != None:
                content = f_handle.read()
                textbox.insert(1.0, content)
        except Exception as e:
            self.log(f"There was an error opening {filename}")
            self.log(e)
            return
        return f_handle

    def log(self, msg):
        print(msg)

        
            
        


root = Tk()
app = App(root)
root.mainloop()
