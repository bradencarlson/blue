#!/bin/bash

# Need to process options, 
# this should include some file names, and 
# what operations that need to be performed, 
# such as 
#    - file comparison
#    - printing out matches 
#    - printing out (dis?)matches

SCRIPT_NAME="link-crew.sh"
VERSION="0"
HELP_MESSAGE="""This is $SCRIPT_NAME v$VERSION\n\n
Usage: $SCRIPT_NAME [options]\n
\n
Available options:\n
    -h, --help: Display this text.\n
""" 

MASTER_FILE=""
ACCEPTED_FILE=""
RECOMMENDED_FILE=""

MASTER_FLAG=0
ACCEPTED_FLAG=0
RECOMMENDED_FLAG=0
SKIP_LINE_ENDING_CHECK=0

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
        fi

        # process other options
        if [[ $opt == "-h" || $opt == "--help" ]]; then 
                echo -e $HELP_MESSAGE
                exit;
        elif [[ $opt == "--master" ]]; then
                MASTER_FLAG=1
        elif [[ $opt == "--accepted" ]]; then 
                ACCEPTED_FLAG=1
        elif [[ $opt == "--recommended" ]]; then 
                RECOMMENDED_FLAG=1
        elif [[ $opt == "--skip-line-endings" ]]; then
                SKIP_LINE_ENDING_CHECK=1
        fi
done

