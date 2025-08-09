""" colors.py
Author: Braden Carlson

Defines the colors which are used throughout the application.  Defining them
here makes it easier to change things later on and customize it. """

BG = "#454545"
BG_ACTIVE = "#757575"
BG_INACTIVE = "#555555"
FG = "#ffffff"
FG_ACTIVE = "#ffffff"
FG_INACTIVE ="#ffffff"

BG_TEXT = "#555555"
FG_TEXT = "#ffffff"
TEXT_INSERT = "#ffffff"

menu_style = {
        'bg': BG, 
        'fg': FG,
        'activebackground': BG_ACTIVE,
        'activeforeground': FG_ACTIVE,
        'bd': 0}

text_style = {
        'bg': BG_TEXT,
        'fg': FG_TEXT,
        'bd': 0,
        'insertbackground': TEXT_INSERT,
        'font': "Ariel 12"}
