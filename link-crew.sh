#!/bin/bash


SCRIPT_NAME="link-crew.sh"
VERSION="0"

# text options
ITALIC="\033[3;80m"
UNDERLINE="\033[4;80m"
NORMAL="\033[0;00m"

# These four control where text is printed vertically on the screen, 
# makes life much easier than entering a bunch of tabs everywhere...
COLUMN1="\033[100D\033[3C"
COLUMN2="\033[100D\033[30C"
COLUMN3="\033[100D\033[35C"
COLUMN4="\033[100D\033[40C"
HELP_MESSAGE="This is $SCRIPT_NAME v$VERSION\n\n
Usage: $SCRIPT_NAME [options]\n
\n
Available options:\n
$COLUMN1 -h, --help: $COLUMN2 Display this text.\n
$COLUMN1 --master ${UNDERLINE}file$NORMAL $COLUMN2 Use ${UNDERLINE}file$NORMAL as the master file.\n
$COLUMN1 --recommended ${UNDERLINE}file$NORMAL $COLUMN2 Use ${UNDERLINE}file$NORMAL as the recommended file.\n
$COLUMN1 --accepted ${UNDERLINE}file$NORMAL $COLUMN2 Use ${UNDERLINE}file$NORMAL as the accepted file.\n
$COLUMN1 --skip-line-endings $COLUMN2 Don't correct line endings of files provided.\n
$COLUMN1 -d, --difference 1 - 2 $COLUMN2 Take a difference between option 1 and option 2.\n
                $COLUMN2 This will take each line in option 1 and search for a match in option 2.\n
                $COLUMN2 Thus it does not matter if each line in option 2 contains more information\n
                $COLUMN2 then the lines in option 1, but if no line in option 2 contains the exact text\n
                $COLUMN2 in the line from option 1 this will result in a failure to match, and that line\n
                $COLUMN2 will be saved in the ${ITALIC}--no-match$NORMAL file if provided, otherwise, they will be\n
                $COLUMN2 printed to the screen.\n
                $COLUMN3 options 1 and 2 may be any of the following:\n
                $COLUMN4 accepted, master, recommended.\n
$COLUMN1 -c, --capitalize ${UNDERLINE}file$NORMAL $COLUMN2 Goes through the provided ${UNDERLINE}file$NORMAL and capitalizes the beginning\n
                $COLUMN2 of EACH word, so it is important that this option be used only\n
                $COLUMN2 on files that contain lists of names.\n
$COLUMN1 -m, --match ${UNDERLINE}file$NORMAL $COLUMN2 File to use to print matching lines, if an appropriate operation\n
                $COLUMN2 is given.\n
$COLUMN1 -n, --no-match ${UNDERLINE}file$NORMAL $COLUMN2 File to use to print unmatching lines, if an appropriate operation\n
                $COLUMN2 is given.\n
" 

# files
BACKUP_DIR="backups"
MASTER_FILE=""
ACCEPTED_FILE=""
RECOMMENDED_FILE=""
NO_MATCH_FILE=""
MATCH_FILE=""
CAPITALIZE_FILE=""

MASTER_FLAG=0
ACCEPTED_FLAG=0
RECOMMENDED_FLAG=0
NO_MATCH_FLAG=0
MATCH_FLAG=0
DIFFERENCE_FLAG=0
DIFFERENCE_ARG_FLAG=0
CAPITALIZE_FLAG=0
SKIP_LINE_ENDING_CHECK=0

DIFF_ARG0=""
DIFF_ARG1=""
DIFF_SEP="-"

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
                echo -e $HELP_MESSAGE
                exit 0;
        elif [[ $opt == "--master" ]]; then
                MASTER_FLAG=1
        elif [[ $opt == "--accepted" ]]; then 
                ACCEPTED_FLAG=1
        elif [[ $opt == "--recommended" ]]; then 
                RECOMMENDED_FLAG=1
        elif [[ $opt == "--skip-line-endings" ]]; then
                SKIP_LINE_ENDING_CHECK=1
        elif [[ $opt == "--difference"  || $opt == "-d" ]]; then
                DIFFERENCE_FLAG=1
                ACTIONS[$POS]="diff"
                POS=$(($POS + 1))
        elif [[ $opt == "--match" || $opt == "-m" ]]; then 
                MATCH_FLAG=1
        elif [[ $opt == "--no-match" || $opt == "-n" ]]; then 
                NO_MATCH_FLAG=1
        elif [[ $opt == "--capitalize" || $opt == "-c" ]]; then 
                CAPITALIZE_FLAG=1
                ACTIONS[$POS]="capitalize"
                POS=$(($POS + 1))
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
                [[ ! -z $1 ]] && [[ -f $1 ]] && sed -E -i.bak 's/\r//g' $1;
        fi
}

fix_line_endings $MASTER_FILE
fix_line_endings $RECOMMENDED_FILE
fix_line_endings $ACCEPTED_FILE

## Helper functions

capitalize_names() {
        [[ ! -z $1 ]] && [[ -f $1 ]] && sed -Ei.before_caps 's/\<([a-z])([a-z]*)\>/\u\1\2/g' $1
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
                        FOUND=$(grep "$line" < $2)
                        if [[ -z $FOUND ]]; then 
                                if [[ -z $NO_MATCH_FILE ]]; then 
                                        echo $line
                                else 
                                        echo $line >> $NO_MATCH_FILE
                                fi
                        else
                                [[ ! -z $MATCH_FILE ]] && echo $line >> $MATCH_FILE
                        fi
                done < $1
        else 
                echo "Something went wrong with the comparison... Maybe double check the file\nnames you used?\nExiting now..."
                exit 1;
        fi
}


for action in ${ACTIONS[@]}; do
        case ${ACTIONS[@]} in
                "diff")
                        if [[ $DIFF_ARG0 == "accepted" && $DIFF_ARG1 == "master" ]]; then
                                comparison $ACCEPTED_FILE $MASTER_FILE
                        elif [[ $DIFF_ARG0 == "recommended" && $DIFF_ARG1 == "accepted" ]]; then 
                                comparison $RECOMMENDED_FILE $ACCEPTED_FILE
                        elif [[ $DIFF_ARG0 == "accepted" && $DIFF_ARG1 == "recommended" ]]; then 
                                comparison $ACCEPTED_FILE $RECOMMENDED_FILE
                        fi
                        ;;
                "capitalize")
                        capitalize_names $CAPITALIZE_FILE
                        ;;
                *)
                        ;;
        esac
                
done

echo "Running clean up..."
clean_up
