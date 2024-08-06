#!/bin/bash

# link-crew.sh 
# Written By: Braden Carlson 
# Date: April 2024
#
# You should have received a copy of the README file along with this script. 
# Please read over it for a full description and some examples. 
#
# This script was written for use in the link crew program, to solve the
# task of taking a list of students who had been accepted as link crew leaders 
# and comparing it to a list of students who had been recommended by faculty. 
# This script can also perform the same comparison on students who have 
# been recommended but are not on an applied list. Another application of 
# this script is to take a list of students and extract their information from 
# a 'master' file, which may contain more information such as a parent's email. 
#
# This script can also take a list of names and correct any capitalization 
# mistakes that are found in the script.  Run this script with the -h or --help 
# option to get started. 
#
# See bottom for license information.


SCRIPT_NAME="link-crew.sh"
VERSION="0"

# text options
ITALIC="\e[3;0m"
UNDERLINE="\e[4;0m"
NORMAL="\e[0;0m"
BOLD="\e[1;0m"

EMPH="\e[1;31m"
KEYWORD="\e[1;33m"

# These four control where text is printed vertically on the screen, 
# makes life much easier than entering a bunch of tabs everywhere...
COLUMN1="\033[100D\033[3C"
COLUMN2="\033[100D\033[30C"
COLUMN3="\033[100D\033[35C"
COLUMN4="\033[100D\033[40C"

# What to display when help is requested. 
HELP_MESSAGE="""This is $SCRIPT_NAME v$VERSION\n
Usage: $SCRIPT_NAME [options]

This script is designed for use with three lists of students, namely
$COLUMN1 - recommended
$COLUMN1 - accepted
$COLUMN1 - master
The recommended and accepted lists should simply be lists of names, while
the master list must contain a column which matches up with the information
found in the recommended and/or accepted list, which will be used for comparing
the two files and finding matches and differences.\n
${EMPH}Please make sure data is clean (no extra spaces please) before using this script.${NORMAL}\n
This script can perform a few data cleaning tasks, such as correcting line endings to UNIX style, 
and capitalizing the first letter of each word (useful for the accepted and recommended lists).\n
Available options:
$COLUMN1 -h, --help $COLUMN2 Display this text.
$COLUMN1 -m, --master ${KEYWORD}file$NORMAL $COLUMN2 Use ${KEYWORD}file$NORMAL as the master file.
$COLUMN1 -r, --recommended ${KEYWORD}file$NORMAL $COLUMN2 Use ${KEYWORD}file$NORMAL as the recommended file.
$COLUMN1 -a, --accepted ${KEYWORD}file$NORMAL $COLUMN2 Use ${KEYWORD}file$NORMAL as the accepted file.
$COLUMN1 --skip-line-endings $COLUMN2 Don't correct line endings of files provided.
$COLUMN1 -d, --difference ${KEYWORD}1 - 2$NORMAL $COLUMN2 Take a difference between option ${KEYWORD}1$NORMAL and option ${KEYWORD}2$NORMAL.
                $COLUMN2 This will take each line in option ${KEYWORD}1$NORMAL and search for a match in option ${KEYWORD}2$NORMAL.
                $COLUMN2 Thus it does not matter if each line in option ${KEYWORD}2$NORMAL contains more information
                $COLUMN2 then the lines in option 1, but if no line in option ${KEYWORD}2$NORMAL contains the exact text
                $COLUMN2 in the line from option ${KEYWORD}1$NORMAL this will result in a failure to match, and that line
                $COLUMN2 will be saved in the ${ITALIC}--no-match$NORMAL file if provided, otherwise, they will be
                $COLUMN2 printed to the screen.
                $COLUMN3 options ${KEYWORD}1$NORMAL and ${KEYWORD}2$NORMAL may be any of the following:
                $COLUMN4 accepted, master, recommended.
$COLUMN1 -c, --capitalize ${KEYWORD}file$NORMAL $COLUMN2 Goes through the provided ${KEYWORD}file$NORMAL and capitalizes the beginning
                $COLUMN2 of ${EMPH}EACH$NORMAL word, so it is important that this option be used only
                $COLUMN2 on files that contain lists of names.
$COLUMN1 --match ${KEYWORD}file$NORMAL $COLUMN2 File to use to print matching lines, if an appropriate operation
                $COLUMN2 is given.
$COLUMN1 -n, --no-match ${KEYWORD}file$NORMAL $COLUMN2 File to use to print unmatching lines, if an appropriate operation
                $COLUMN2 is given.
$COLUMN1 --backup $COLUMN2 Backup all files before changing them in any way. 
""" 

# files
BACKUP_DIR="backups"
MASTER_FILE=""
ACCEPTED_FILE=""
RECOMMENDED_FILE=""
NO_MATCH_FILE=""
MATCH_FILE=""
CAPITALIZE_FILE=""

# flags
MASTER_FLAG=0
ACCEPTED_FLAG=0
RECOMMENDED_FLAG=0
NO_MATCH_FLAG=0
MATCH_FLAG=0
DIFFERENCE_FLAG=0
DIFFERENCE_ARG_FLAG=0
CAPITALIZE_FLAG=0
BACKUP_FLAG=0
SKIP_LINE_ENDING_CHECK=0

# difference arguments
DIFF_ARG0=""
DIFF_ARG1=""
DIFF_SEP="-"

# actions list. 
ACTIONS=()
POS=0

for opt in $@; do
        # process flags
        if [[ $MASTER_FLAG == 1 ]]; then 
                MASTER_FILE=$opt
                MASTER_FLAG=0
                continue
        elif [[ $RECOMMENDED_FLAG == 1 ]]; then
                RECOMMENDED_FILE=$opt
                RECOMMENDED_FLAG=0
                continue
        elif [[ $ACCEPTED_FLAG == 1 ]]; then 
                ACCEPTED_FILE=$opt
                ACCEPTED_FLAG=0
                continue
        elif [[ $DIFFERENCE_FLAG == 1 ]]; then 
                DIFF_ARG0=$opt
                DIFFERENCE_FLAG=0
                DIFFERENCE_ARG_FLAG=1
                continue
        elif [[ $DIFFERENCE_ARG_FLAG == 1 && $opt == $DIFF_SEP ]]; then 
                continue
        elif [[ $DIFFERENCE_ARG_FLAG == 1 ]]; then
                DIFF_ARG1=$opt
                DIFFERENCE_ARG_FLAG=0
                continue
        elif [[ $MATCH_FLAG == 1 ]]; then 
                MATCH_FLAG=0
                MATCH_FILE=$opt
                continue
        elif [[ $NO_MATCH_FLAG == 1 ]]; then 
                NO_MATCH_FLAG=0
                NO_MATCH_FILE=$opt
                continue
        elif [[ $CAPITALIZE_FLAG == 1 ]]; then 
                CAPITALIZE_FLAG=0
                CAPITALIZE_FILE=$opt
                continue
        fi

        # process other options
        if [[ $opt == "-h" || $opt == "--help" ]]; then 
                printf "$HELP_MESSAGE"
                exit 0;
        elif [[ $opt == "--master" || $opt == "-m"  ]]; then
                MASTER_FLAG=1
        elif [[ $opt == "--accepted" || $opt == "-a" ]]; then 
                ACCEPTED_FLAG=1
        elif [[ $opt == "--recommended" || $opt == "-r" ]]; then 
                RECOMMENDED_FLAG=1
        elif [[ $opt == "--skip-line-endings" ]]; then
                SKIP_LINE_ENDING_CHECK=1
        elif [[ $opt == "--difference"  || $opt == "-d" ]]; then
                DIFFERENCE_FLAG=1
                ACTIONS[$POS]="diff"
                POS=$(($POS + 1))
        elif [[ $opt == "--match" ]]; then 
                MATCH_FLAG=1
        elif [[ $opt == "--no-match" || $opt == "-n" ]]; then 
                NO_MATCH_FLAG=1
        elif [[ $opt == "--capitalize" || $opt == "-c" ]]; then 
                CAPITALIZE_FLAG=1
                ACTIONS[$POS]="capitalize"
                POS=$(($POS + 1))
        elif [[ $opt == "--backup" ]]; then 
                BACKUP_FLAG=1
        else
                echo "Invalid argument: $opt"
                echo "exiting..."
                exit 1;
        fi
done

# Check to make sure that the files provided actually exist. 
test_file_exists() {
        if [[ ! -z $1 ]]; then 
                if [[ ! -f $1 ]]; then 
                        echo "$1 does not exist... exiting"
                        exit 1;
                fi
        fi
}

test_file_exists $MASTER_FILE
test_file_exists $RECOMMENDED_FILE
test_file_exists $ACCEPTED_FILE

# strip \r from each file, to convert to unix line endings, unless
# the --skip-line-endings option was provided. 

fix_line_endings() {
        if [[ $SKIP_LINE_ENDING_CHECK == 0 ]]; then 
                if [[ $BACKUP_FLAG == 1 ]]; then 
                        [[ ! -z $1 ]] && [[ -f $1 ]] && sed -E -i.bak 's/\r//g' $1;
                else 
                        [[ ! -z $1 ]] && [[ -f $1 ]] && sed -E -i 's/\r//g' $1;
                fi
        fi
}

fix_line_endings $MASTER_FILE
fix_line_endings $RECOMMENDED_FILE
fix_line_endings $ACCEPTED_FILE

## Helper functions

capitalize_names() {
        if [[ $BACKUP_FLAG == 1 ]]; then
                [[ ! -z $1 ]] && [[ -f $1 ]] && sed -Ei.before_caps 's/\<([a-z])([a-zA-Z]*)\>/\u\1\L\2/g' $1
        else 
                [[ ! -z $1 ]] && [[ -f $1 ]] && sed -E -i 's/\<([a-z])([a-zA-Z]*)\>/\u\1\L\2/g' $1
        fi
}

clean_up() {
        mkdir $BACKUP_DIR 2>/dev/null
        mv -f *.bak $BACKUP_DIR/ 2>/dev/null
        mv -f *.before_caps $BACKUP_DIR/ 2>/dev/null
}


# runs a comparison between arguments $1 and $2, that is searches 
# for each line in $1 in $2 and performs the appropriate action. 
comparison() {
        if  [[ -f $1 && -f $2 ]]; then 
                while IFS= read -r line; do
                        line=$(echo $line | sed 's/\r//g; s/\n//g')
                        FOUND=$(grep "$line" < $2)
                        if [[ -z $FOUND ]]; then 
                                if [[ -z $NO_MATCH_FILE ]]; then 
                                        echo $line
                                else 
                                        echo $line >> $NO_MATCH_FILE
                                fi
                        else
                                [[ ! -z $MATCH_FILE ]] && echo "$FOUND" >> $MATCH_FILE
                        fi
                done < $1
        else 
                echo "Something went wrong with the comparison... Maybe double check the file\nnames you used?\nExiting now..."
                exit 1;
        fi
}

# process actions
for action in ${ACTIONS[@]}; do
        case ${ACTIONS[@]} in
                "diff")
                        if [[ $DIFF_ARG0 == "accepted" && $DIFF_ARG1 == "master" ]]; then
                                comparison $ACCEPTED_FILE $MASTER_FILE
                        elif [[ $DIFF_ARG0 == "recommended" && $DIFF_ARG1 == "accepted" ]]; then 
                                comparison $RECOMMENDED_FILE $ACCEPTED_FILE
                        elif [[ $DIFF_ARG0 == "accepted" && $DIFF_ARG1 == "recommended" ]]; then 
                                comparison $ACCEPTED_FILE $RECOMMENDED_FILE
                        elif [[ $DIFF_ARG0 == "recommended" && $DIFF_ARG1 == "master" ]]; then 
                                comparison $RECOMMENDED_FILE $MASTER_FILE
                        else 
                                echo -e "Looks like the difference operation you requested is\nnot valid... exiting."
                                exit 1;
                        fi
                        ;;
                "capitalize")
                        capitalize_names $CAPITALIZE_FILE
                        ;;
                *)
                        ;;
        esac
                
done

# clean up backups if necessary. 
if [[ $BACKUP_FLAG == 1 ]]; then
        echo "Running clean up..."
        clean_up
        echo "All backups can be found in the 'backups' directory."
fi


# Copyright 2024 Braden Carlson
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# “Software”), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
