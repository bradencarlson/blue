"""
Author: Braden Carlson
Date: June 2025

This module provides the File OPerationS (fops) that the user 
will need while useing this application. 
"""

import re

def sort_lines(lines):
    """ sorts an array of strings by alphabetical order. """
    return lines.sort()

def capitalize(string):
    string = re.sub(r"/([a-zA-Z]+)/",lambda m: m.group(0).capitalize(), string)
    return string
