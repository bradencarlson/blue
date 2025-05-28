from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from graphic_elements import *

class App(ttk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.current_filename = ""

        # define menu dictionary for the top of the window
        menu_dict = {"File": {"New": partial(self.log,"New clicked"), 
                              "Open": partial(self.log, "Open clicked")},
                     "Edit": {"Copy": partial(self.log, "Copy clicked"),
                              "Paste": partial(self.log,"Paste clicked")}};
        createMenubar(master, menu_dict)

        frm = createLogo(master)
        [fileArea, text1] = createFileArea(master)
        btn = ttk.Button(frm, text="Open File", 
                         command=partial(self.open_file, "NONE",textbox=text1))
        btn.grid(row=0, column=1)

        save_btn = ttk.Button(frm, text="Save File", 
                              command=partial(self.save_file,textbox=text1))
        save_btn.grid(row=0,column=2)
        frm.grid(row=0,column=0,sticky="W")
        fileArea.grid(row=1, column=0)

        

    def open_file(self, filename, permissions="r", textbox= None):
        if filename == "NONE":
            filename = filedialog.askopenfilename()

        try:
            f_handle = open(filename, permissions)
            self.current_filename = filename
            if textbox != None:
                content = f_handle.read()
                textbox.delete(1.0,END)
                textbox.insert(1.0, content)
        except Exception as e:
            self.log(f"There was an error opening {filename}")
            self.log(e)
            return
        return f_handle

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

        f_handle.write(textbox.get(1.0,END));


    def log(self, msg):
        print(msg)

        
            
        


root = Tk()
app = App(root)
root.mainloop()
