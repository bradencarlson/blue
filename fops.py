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
    new = '\n'.join(lines)
    return new


def capitalize_words(string):
    """ Capitalize each word (defined as any string of alphbetic chars) of the
    parameter. """

    string = re.sub(r"([a-zA-Z]+)",lambda m: m.group(0).capitalize(), string)
    return string

def difference(file1, file2, **opts):
    """ Find each line of file1 which does not appear in file2, regardless of
    the order of lines in each file.  This is different than diff, which
    compares files line by line. """

    matches = []
    nonmatches = []

    try:
        with open(file1,"r") as f1:
            f2 = open(file2, "r")
            f2_text = f2.read()
            line = f1.readline()
            while line: 
                line = line.removesuffix('\n')
                match = re.findall(line, f2_text)
                if len(match) == 0:
                    nonmatches.append(line)
                else: 
                    matches.append(line)
                line = f1.readline()
    except Exception as e:
        print(e)

    return nonmatches
