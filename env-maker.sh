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
VIRTUALENV_DIR=${1:-venv}
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

if [[ $MINIMUM_TARGET_VERSION -ge $CURRENT_VERSION ]] || [ "$(python3_exists)" == 0 ]; then
    echo "${RED}The minimum Python version (which is $MINIMUM_TARGET_VERSION) isn't installed.${RESET}";
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
    echo "${RED}Or, if you want to create a new one, delete the current virtualenv (rm -rf \"${VIRTUALENV_DIR}\") and run the script again.${RESET}"

    echo "${CYAN}Skipping virtualenv configuration.${RESET}"
    source "${VIRTUALENV_DIR}/bin/activate"
    SHOW_VIRTUALENV_MESSAGE="0"
fi

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
        fi
    fi

    echo "${CYAN}Pulling updates...${RESET}"
    git pull --rebase origin master
    echo "${GREEN}Done!${RESET}"

    if [[ -f "$POST_MERGE_HOOK_FILE" ]]; then
        SHOULD_INSTALL="0"
    fi
fi

if [[ ! -f "$POST_MERGE_HOOK_FILE" ]]; then
mkdir -p .git/hooks

echo "${CYAN}Creating \"post-merge\" hook on ${POST_MERGE_HOOK_FILE}.${RESET}"
cat << EOF > "$POST_MERGE_HOOK_FILE"
#!/usr/bin/env python3
import sys
from subprocess import call

from data_mass.classes.text import text


print(text.Cyan + "Updating data mass..." + text.Default)
exit_code = call(["pip3 install ."], shell=True)

if not exit_code:
    print(text.Green + "Done!" + text.Default)
else:
    print(text.Red + "Error while updating Data Mass.")
    print("Update manually by doing:\n")
    print("pip install .")

EOF
    chmod +x .git/hooks/post-merge
    echo "${GREEN}Done!${RESET}"
fi

if [ $SHOULD_INSTALL == "1" ]; then
    echo "${CYAN}Installing Data Mass...${RESET}"

    if [[ $(pip -V | grep ${VIRTUALENV_DIR}) ]]; then
        python3 setup.py install --force
    else
        python3 setup.py install --user --force
    fi

    python3 -m pip install .
    echo "${GREEN}Done!${RESET}"
fi


if [ $SHOW_VIRTUALENV_MESSAGE == "1" ]; then
    echo "${CYAN}NOTE: to start the virtualenv, run \"source $VIRTUALENV_DIR/bin/activate\".${RESET}"
fi
