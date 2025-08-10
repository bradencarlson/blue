""" fops.py
Author: Braden Carlson
Date: June 2025

This module provides the File OPerationS (fops) that the user 
will need while useing this application. 
"""

import re
from dialog import error

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
        with open(file1,"r",encoding="utf-8") as f1:
            with open(file2, "r", encoding="utf-8") as f2:
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
    except FileNotFoundError:
        error(None,msg=f"One of {file1} or {file2} does not exist.")

    return nonmatches

def strip(string, char):
    """ Strips all instances of char in string. """

    lines = string.splitlines()

    new_lines = []
    for line in lines:
        new_line = re.sub(char, '', line)
        new_lines.append(new_line)

    return '\n'.join(new_lines)


def get_num_fields(lines, **opts):
    """ Get the smalled number of records which appears in any line of the file.
    This is used in the cut method to ensure that the range attained from the
    user does not go out of bounds. """

    max_number_of_records = 1000

    try:
        fs = opts['FS']
    except KeyError:
        fs = ","

    mnr = max_number_of_records
    lineno= 1
    index = 1
    for line in lines:
        records = re.split(fs, line)
        if len(records) <= mnr:
            mnr = len(records)
            lineno = index
        index = index + 1

    if lineno < len(lines):
        error(None, f"There is probably a problem with the data, check line number {lineno}")
    return [mnr, lineno]

def cut(string, **opts):
    """ Mini implementation of the cut command from Linux. """

    lines = string.splitlines()
    new_lines = []

    try:
        fs = opts['fs']
    except KeyError:
        fs = ","

    mnr = get_num_fields(lines, fs=fs)[0]

    if 'f' in opts.keys():
        nums = parse_num_range(opts['f'])
        max_num = max(nums)
        if max_num > mnr:
            print("invalid range given")
            return '\n'.join(lines)

        index = 1
        for line in lines:
            records = re.split(fs, line)
            nr = len(records)
            if max_num > nr:
                print(f"There was an error on line {index}")
                return '\n'.join(lines)
            new_line = fs.join([records[i-1] for i in nums])
            new_lines.append(new_line)
            index = index + 1
        new_string = '\n'.join(new_lines)
        return new_string


def parse_num_range(rng):
    """ Take a string, which represents a range of of numbers, and return a list
    of the numbers in that range. """

    def parse_range(r):
        """ This method actually does the parsing of the range. It takes a
        single range (i.e. 3-5) and returns all numbers in that range as an
        array (i.e. [3,4,5]). """

        num1 = re.search(r'^[0-9]+',r)
        num2 = re.search(r'-?[0-9]*$',r)

        if num1 is None:
            return 0

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

    nums = []

    rng = re.sub(r'\s+','',rng)

    if re.search(r',',rng):
        lst = re.split(r',', rng)
        for r in lst:
            [start, end] = parse_range(r)
            for i in range(start, end + 1):
                nums.append(i)
    else:
        [start, end] = parse_range(rng)
        for i in range(start, end + 1):
            nums.append(i)

    return nums
