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

# Colors
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
CYAN=`tput setaf 6`
RESET=`tput sgr0`

function python3_exists() {
    command -v python3 || { echo "0"; }
}

if [[ $MINIMUM_TARGET_VERSION > $CURRENT_VERSION ]] || [ "$(python3_exists)" == 0 ]; then
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
fi

echo "${CYAN}Fetching Data Mass updates...${RESET}"
# git fetch

REMOTE=$(git rev-parse origin/master)

if [[ ! $(git log | grep ${REMOTE}) ]]; then
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

    if [[ $(ls .git/hooks | grep "post-merge") ]]; then
        SHOULD_INSTALL="0"
    fi
fi

if [ ! -d ".git/hooks/post-merge" ]; then
cat << EOF > post-merge
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
    mv post-merge .git/hooks/
    chmod +x .git/hooks/post-merge
fi

if [ $SHOULD_INSTALL == "1" ]; then
    echo "${CYAN}Installing Data Mass...${RESET}"
    python3 -m pip install .
    echo "${GREEN}Done!${RESET}"
fi

echo "${CYAN}NOTE: to start the virtualenv, run \"source $VIRTUALENV_DIR/bin/activate\".${RESET}"
