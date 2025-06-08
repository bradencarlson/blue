from tkinter import *
from tkinter import ttk
from graphic_elements import *
import colors as color
import dialog as dialog

class Link(Widget):


    def __init__(self, master):
        super().__init__(master,'frame')
        # Save this so I can add the menu to the top level widget.
        self.master = master

        self.notebook = LinkNotebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True)

        menu_dict = {"View": {'Add Tab': self.addTab}}
        self.createMenu(menu_dict)

    # Create a menu from a dictionary. See the createMenu method in the LinkTab
    # class in the graphic_elements file. 
    def createMenu(self, menu_dict):
        menu = Menu(self,tearoff=0,**color.menu_style)
        pos = 0
        for label, submenu_dict in menu_dict.items():
            submenu = Menu(menu,tearoff=0,**color.menu_style)
            for sub_label, command in submenu_dict.items():
                submenu.add_command(label=str(sub_label), command=command)
            menu.add_cascade(label=label, menu=submenu)
        self.master.config(menu=menu)

    def addTab(self,**kwargs):

        # KEYWORD ARGS

        # kind - what kind of tab to add
        # label - what the tab should be labeled. 

        try: 
            self.notebook.addTab(kind=kwargs['kind'], 
                                 text=kwargs['label'])
        except Exception as e:
            [label, kind] = dialog.askNewTab(self)
            self.notebook.addTab(kind=kind, text=label)

    # Wrapper for the tabs method of the LinkNotebook class 
    def tabs(self):
        return self.notebook.tabs()

    # Wrapper for the tab method of the LinkNotebook class
    def tab(self,index):
        return self.notebook.tab(index)

    # Wrapper for select method of LinkNotebook class
    def select(self,index=None):
        return self.notebook.select(index)


        
            
#root = Tk()
#root.configure(bg=color.bg)
#app = Link(root)
#root.mainloop()
