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

def cut(filename, **opts):
    """ Mini implementation of the cut command from Linux. """

    try: 
        FS = opts['FS']
    except KeyError: 
        FS = ","

    if 'f' in opts.keys():
        nums = parse_num_range(opts['f'])

def parse_num_range(rng):
    """ Take a string, which represents a range of of numbers, and return a list
    of the numbers in that range. """

    def parse_range(r):
        num1 = re.search(r'^[0-9]+',r)
        num2 = re.search(r'-?[0-9]*$',r)

        num1_start = num1.span()[0] # Should always be zero. 
        num2_start = num2.span()[0]

        num1_length = num1.span()[1]-num1.span()[0]

        if num1_start == num2_start:
            start = int(r[num1_start:num1_length ])
            return [start, start]

        # Minus one here since the match includes the 
        num2_length = num2.span()[1] - num2.span()[0] - 1

        start = int(r[num1_start: num1_start + num1_length])
        end = int(r[num2_start + 1: num2_start +1 + num2_length ])

        return [start, end]

        
    ranges = []

    rng = re.sub(r'\s+','',rng)
    print(rng)

    if re.search(r',',rng):
        lst = re.split(r',', rng)
        for r in lst: 
            [start, end] = parse_range(r)
            ranges.append(list(range(start, end + 1)))

    return ranges
