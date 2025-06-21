"""
Author: Braden Carlson
Date: June 2025

This module provides the File OPerationS (fops) that the user 
will need while useing this application. 
"""

import re

def sort_lines(string):
    """ sorts lines in a string. """

    lines = list(string.splitlines() or [])
    lines.sort()
    print(lines)
    new = '\n'.join(lines)
    return new


def capitalize_words(string):
    """ Capitalize each word (defined as any string of alphbetic chars) of the
    parameter. """

    string = re.sub(r"([a-zA-Z]+)",lambda m: m.group(0).capitalize(), string)
    return string
