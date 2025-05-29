from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from graphic_elements import *

class Link(ttk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.current_filename = ""
        self.current_message = "sample message"
        self.message_textbox = None


        notebook = LinkNotebook(master)
        notebook.addTab(kind="TextTab", text="hi")

        new_menu = {"Operations": {"Close": root.quit}}
        notebook.addTab(kind="TextTab", text="hello", menu=new_menu)
        notebook.grid(row=0, column=0)

        

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
