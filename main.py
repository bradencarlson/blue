""" main.py
Author: Braden Carlson <bradenjcarlson@live.com>

Defines the Link class, which is the top level widget after root to be called
when implementing this application. This class contains a ttk.Notebook child,
which contains tabs for files, as well as tabs for file operations. Everything
that can be done with this program should be able to be performed both
graphically as well as programmatically, in a simple easy to understand manner.
Therefor, many of the methods in this class are simply wrappers to their
corresponding methods in the TextTab and OperationTab classes which are the
children of the Notebook contained in this class.  """

from tkinter import Widget, Menu
from graphic_elements import LinkNotebook
import colors as color
import dialog as dlg

class Link(Widget):
    """ Main Widget to be placed on the root window for the application.
    This class contains a LinkNotebook which holds all the tabs needed to
    perform the tasks necessary. It also holds the menu for the application, so
    the root window should not have a menu added to it. """

    def __init__(self, master):
        super().__init__(master,'frame')
        # Save this so I can add the menu to the top level widget.
        self.master = master

        self.notebook = LinkNotebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True)

        menu_dict = {"Blue": {'Close': self.close},
                     "View": {'Add Tab': self.add_tab}}
        self.create_menu(menu_dict)

    def create_menu(self, menu_dict):
        """ Create a menu from a dictionary. See the create_menu method in the LinkTab
        class in the graphic_elements file. """
        menu = Menu(self,tearoff=0,**color.menu_style)
        for label, submenu_dict in menu_dict.items():
            submenu = Menu(menu,tearoff=0,**color.menu_style)
            for sub_label, command in submenu_dict.items():
                submenu.add_command(label=str(sub_label), command=command)
            menu.add_cascade(label=label, menu=submenu)
        self.master.config(menu=menu)

    def add_tab(self,**kwargs):
        """ Adds a tab to the LinkNotebook. If the proper keyword arguments are
        not passed to this method, then the application will open a NewTabDialog
        which will prompt the user for the name of the tab and what kind of tab
        it should be. """

        # KEYWORD ARGS

        # kind - what kind of tab to add
        # label - what the tab should be labeled.

        try:
            self.notebook.add_tab(kind=kwargs['kind'],
                                 text=kwargs['label'])
        except KeyError:
            [label, kind] = dlg.ask_new_tab(self)
            self.notebook.add_tab(kind=kind, text=label)

    def tabs(self):
        """ Wrapper for the tabs method of the LinkNotebook class """
        return self.notebook.tabs()

    def tab(self,index):
        """ Wrapper for the tab method of the LinkNotebook class """
        return self.notebook.tab(index)

    def select(self,index=None):
        """ Wrapper for select method of LinkNotebook class """
        return self.notebook.select(index)

    def close(self):
        """ Quit the applitation """
        super().quit()

    def current_tab(self):
        """ Return the currently selected tab. This returns the actual object,
        so that it's methods can be called. """

        tab_id = self.notebook.select()
        index = self.notebook.index(tab_id)
        return self.notebook.get_tab(index)

    def get_tab(self, index):
        """ Similar to the current_tab method, but returns the tab at the
        specified index. """

        return self.notebook.get_tab(index)
