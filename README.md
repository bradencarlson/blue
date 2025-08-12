# Blue

<span style="nowrap">
<img alt="Linted with Pylint" src="https://img.shields.io/badge/pylint-9.69-blue">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/bradencarlson/blue"
</span>

## Description

This program was developed to address some common data processing problems
encountered in the Link Crew program at Lewiston High School, specifically to
create a solution which is user friendly (not just pointing to the `cut`,
`sed`, or `awk` programs). Such problems included: fixing capitalization of names 
of student applicants, cutting out unnecessary columns of data, and performing
differences of files (for example, finding all names of students who applied to the
program, but are not listed in some master file of 10th and 11th graders).

## History

This project began as a simple script that I wrote for myself to perform these
tasks, directly relying upon the programs mentioned in the description. This
script is still included in the project.  However, as the years went on I wanted
to be able to leave behind something that anyone could use to perform the same
tasks, and here we are. 

## Examples

The following are examples of using the script that I originally wrote for
myself.

Use `accepted.txt` as the list of accepted students, `recommended.txt` as the 
list of the recommended students, and find the students who are on the 
recommended list but not on the accepted list. 

> link-crew.sh -a accepted.txt -r recommended.txt -d recommended - accepted

Just as the previous example, but print the *matching* names (that is, the names 
on recommended which are found in accepted) to the file `matches.txt`

> link-crew.sh -a accepted.txt -r recommended.txt -d recommended - accepted --match matches.txt

The `--no-match` option is used in the same was as the `--match` option, but prints the 
names that are normally printed to the screen to the file provided. 

Fix the capitalization of the list of students in the `accepted.txt` file. 

> link-crew.sh -c accepted.txt

Fix the capitalization of the list of students in the `accepted.txt` file, and make 
a backup of the original.

> link-crew.sh --backup -c accepted.txt

or

> link-crew.sh -c accepted.txt --backup

## Getting Help

Unfortunately, no documentation currently exists, I am working on it!

----------------------------------------

Copyright 2024 Braden Carlson

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the 
“Software”), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
