import subprocess
import sys
import os

from helpers.common import clearTerminal
from classes.text import text

def install_dependencies():
    # Create file path
    path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(path, "requirements.txt")

    # Get a list of installed packages
    reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split("==")[0] for r in reqs.split()]

    # Check if required dependencies are installed
    # If not, install them
    if "requests" and "jsonpath-rw-ext" and "jsonpath-rw" not in installed_packages:
        print(text.Red + "Dependencies are not installed!" + text.White +  "\nRunning installation...")
        os.system("pip3 install -r" + file_path)
        SclearTerminal()