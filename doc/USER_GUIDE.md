# User Guide
This document describes some Data Mass usage guides.

## Contents:
  - [Contents:](#contents)
    - [Getting logs](#getting-logs)
    - [Using Environment Virtualizer](#using-virtualenv)
    - [Contributing to Data Mass](#contributing-to-data-mass)

### [Getting logs](#getting-logs)
If an error occurs in the application execution, it is necessary to collect the logs for analysis. To do this, follow the instructions below:
1. Check if the `logs` folder was created in `<project-path>/data_mass/`
2. Log subfolders are organized by day, so open the folder with the name referring to the day the log was generated
3. The name of files with the extension `.log` are named with the time they were created, so select the file for the time of execution

It is recommended that you send the complete file, not just the log snippet where the problem occurred.

### [Using Environment Virtualizer](#using-virtualenv)
To keep the environment as pure as possible for using Data Mass, we recommend using [virtualenv](https://pypi.org/project/virtualenv/) to isolate a Python environment on the machine on which the application will run, thus, the default Python on your machine will be affected by Data Mass, and vice versa. To use **virtualenv**, follow the instructions below:
1. Run, using `pip`, the following command:
```bash
pip install virtualenv
```
2. Creating environment with a specific Python version:
```bash
virtualenv -p /usr/bin/python3 venv # "venv" is the name of the directory, you may choose a custom name
```
or
```bash
virtualenv venv # get the default Python version (it must be >=3.7)
```
3. Enabling virtualized Python:
```bash
source the-dir-name-/bin/activate # replace "the-dir-name" with "venv" or, the customized name that you chose
```
4. Disabling virtualized Python:
```bash
deactivate
```

#### [Contributing to Data Mass](#contributing-to-data-mass)
Data Mass has hooks that analyze and evaluate the code, so we can maintain the health of the code. More about hooks, and the way in which they evaluate can be found in the [code style document](C_STYLE_GUIDE.md#overview). To contribute, it is necessary to install the development facilities. Follow the steps below:
1. Install the required development packages:
```bash
pip install requirements-dev.txt
```
2. Install pre-commit into your git hooks:
```bash
pre-commit install
```
You are now able to contribute.
