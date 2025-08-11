#!/bin/bash 

# This is to be run from the base directory of the project. 

pylint $(git ls-files *.py) | grep "has been rated" > temp.file
rate=$(sed -E "/Your/{s@[^0-9]*([0-9\.]+)\/[0-9]+.*@\1@;}" temp.file)
echo ${rate}
sed -Ei "/Linted with Pylint/{s@pylint\-[0-9]+\.?[0-9]*@pylint\-${rate}@;}" README.md
rm temp.file

