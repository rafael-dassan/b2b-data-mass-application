#!/bin/bash

# A simple script to set up the necessary environment to run Data Mass.
# Created and tested in a Linux and MacOS environment.
# If it doesn't work on other OS, help us improve.

# Note: it is recommended that you have AT LEAST Python3 installed.

# Any tips or doubt? Please, let us know!

# Exit the script immediately if a command exits with a non-zero status.
set -e

MINIMUM_TARGET_VERSION="3.7"
RECOMMENDED_VERSION="3.9"
CURRENT_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
VIRTUALENV_DIR="venv"
SHOULD_INSTALL="1"
POST_MERGE_HOOK_FILE=".git/hooks/post-merge"
REMOTE_BRANCH_LAST_COMMIT=$(git rev-parse origin/master)
SHOW_VIRTUALENV_MESSAGE="1"

# Colors
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
CYAN=`tput setaf 6`
RESET=`tput sgr0`

function python3_exists() {
    command -v python3 || { echo "0"; }
}

function install() {
    echo "${CYAN}Installing Data Mass...${RESET}"

    python3 -m pip install .
    echo "${GREEN}Done!${RESET}"
}

function update() {
    echo "${CYAN}Fetching Data Mass updates...${RESET}"
    git fetch
    echo "${GREEN}Done!${RESET}"

    if [[ ! $(git log | grep ${REMOTE_BRANCH_LAST_COMMIT}) ]]; then
        echo "${RED}Your version of Data Mass is out of date.${RESET}"

        if [[ $({ git diff --name-only ; git diff --name-only --staged ; } | sort | uniq) ]]; then
            read -e -p "${RED}You have changed files. Do you want to continue with the update?${RESET} [Y/n] " YN

            if [[ $YN == "y" || $YN == "Y" ]]; then
                echo "${CYAN}Stashing modified files...${RESET}"
                git stash

                echo "${YELLOW}Your modified files are stashed. To recover, use \"git stash apply\".${RESET}"
            else
                echo "${RED}Please, resolve conflicts manually.${RESET}"
                exit 1
            fi
        fi

        echo "${CYAN}Pulling updates...${RESET}"
        git pull --rebase origin master
        echo "${GREEN}Done!${RESET}"
    else
        echo "${GREEN}Your Data Mass source code is up-to-date!${RESET}"
    fi

    if [[ -f "$POST_MERGE_HOOK_FILE" ]]; then
        install
        exit 1
    fi
}

display_usage() {
    echo "usage: $0 [-v] {string} [-u] {True|true|1}" >&2
    echo
    echo "arguments:"
    echo "   -v, --virtualenv           The name of the virtualenv folder. Default to \"venv\""
    echo "   -u, --update-only          Ignore environment creation, only update Data Mass"
    exit 1
}

POSITIONA=()
while [[ $# -gt 0 ]]
do
param="$1"

case $param in 
    -v|--virtualenv)
    VIRTUALENV_DIR="$2"
    shift
    shift
    ;;
    -u|--update-only)
    UPDATE_ONLY="$2"
    shift
    shift
    ;;
    -h|--help)
    display_usage
    shift
    shift
    ;;
    *)
    echo "${RED}Illegal option.${RESET}"
    echo "${CYAN}Use \"--help\" for more details of usage.${RESET}"
    exit 1 
    ;;
esac
done

set -- "${POSITIONAL[@]}"

if [ $UPDATE_ONLY ]; then
    if [ ! -d "venv" ] || [ ! -d $VIRTUALENV_DIR ]; then
        source "${VIRTUALENV_DIR}/bin/activate"
    fi

    update
    install
    exit 1
fi

if (( $(echo $MINIMUM_TARGET_VERSION $CURRENT_VERSION | awk '{if ($1 > $2) print 1;}') )) || [ "$(python3_exists)" == 0 ]; then    echo "${RED}The minimum Python version (which is $MINIMUM_TARGET_VERSION) isn't installed.${RESET}";
    echo "${CYAN}Installing Python version $RECOMMENDED_VERSION, which is the recommended one...${RESET}";
    sudo apt install python+="$TARGET_VERSION"
    
    if [ $(python3_exists) != 0 ]; then
        echo "${GREEN}Python was successfully installed!${RESET}"
    fi
fi

if [ ! -d "venv" ] || [ ! -d $VIRTUALENV_DIR ]; then
    echo "${CYAN}Installing virtualenv...${RESET}"
    python3 -m pip install virtualenv
    echo "${GREEN}virtualenv was successfully installed!${RESET}"

    echo "${CYAN}Virtualizing the Python environment...${RESET}"
    python3 -m virtualenv $VIRTUALENV_DIR -p $(which python3)
    echo "${GREEN}Done!${RESET}"

    echo "${CYAN}Making sure that the latest pip version is being used...${RESET}"
    source "${VIRTUALENV_DIR}/bin/activate"
    python3 -m pip install --upgrade pip
    echo "${GREEN}pip was successfully upgraded!${RESET}"

    echo "${GREEN}Environment has been set up successfully!${RESET}"
else
    echo "${RED}You already have a virtualenv configured!${RESET}"
    echo "${RED}To enable a virtualenv run: \"source $VIRTUALENV_DIR/bin/activate\".${RESET}"
    echo
    echo "${YELLOW}If you want to create a new one, delete the current virtualenv (rm -rf \"${VIRTUALENV_DIR}\") and run the script again.${RESET}"
    echo "${YELLOW}You can also update the Data Mass version of your virtualenv by running this script with the \"--update-only true \" flag.${RESET}"
    echo
    echo "${CYAN}Skipping virtualenv configuration.${RESET}"
    source "${VIRTUALENV_DIR}/bin/activate"
    SHOW_VIRTUALENV_MESSAGE="0"
fi

if [[ ! -f "$POST_MERGE_HOOK_FILE" ]]; then
mkdir -p .git/hooks

echo "${CYAN}Creating \"post-merge\" hook on ${POST_MERGE_HOOK_FILE}.${RESET}"
cat << EOF > "$POST_MERGE_HOOK_FILE"
#!/usr/bin/env python3
import sys
from subprocess import call


print("Updating data mass...")
exit_code = call(["pip3 install ."], shell=True)

if not exit_code:
    print("Done!")
else:
    print("Error while updating Data Mass.")
    print("Update manually by doing:\n")
    print("pip install .")

EOF
    chmod +x .git/hooks/post-merge
    echo "${GREEN}Done!${RESET}"
fi

if [ $SHOW_VIRTUALENV_MESSAGE == "1" ]; then
    install
    echo "${CYAN}NOTE: to start the virtualenv, run \"source $VIRTUALENV_DIR/bin/activate\".${RESET}"
fi
