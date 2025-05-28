from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
from graphic_elements import *

class App(ttk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.current_filename = ""
        self.current_message = "sample message"
        self.message_textbox = None

        # define menu dictionary for the top of the window
        menu_dict = {"File": {"New": partial(self.log,"New clicked"), 
                              "Open": partial(self.log, "Open clicked")},
                     "Edit": {"Copy": partial(self.log, "Copy clicked"),
                              "Paste": partial(self.log,"Paste clicked")}};
        createMenubar(master, menu_dict)

        # Create the logo line, and the file area, 
        # and add two buttons to it (for now), which open
        # and save files. 
        frm = createLogo(master)
        [fileArea, text1] = createFileArea(master)

        frm.grid(row=0,column=0,sticky="W")

        fileArea.grid(row=1, column=0,sticky="W")

        [messageArea,self.message_textbox] = createMessageArea(master)
        messageArea.grid(row=2,column=0,sticky="E")


        

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
app = App(root)
root.mainloop()
