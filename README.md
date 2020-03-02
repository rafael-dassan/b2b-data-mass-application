# B2B Product - Data Mass Script

This repository contains the B2B Data Mass Script, aimed to those who want to create all necessary information to execute tests, develop new features and even explore the apps.

## System Requirements

* Operating system based on UNIX.

## Required Tooling

* [Git][GitDoc]
* [Visual Studio Code][VisualStudioCode]
* [Python 3.x.x][Python]

## Required Libraries

* [Requests][Requests]
* [JSONPath-ext RW][JSONPath-ext RW]
* [JSONPath RW][JSONPath RW]

## Directories structure organization

```sh
data-mass/
├── classes
    └── text.py
├── data
    └── create_account_payload.json
├── helpers
    └── common.py
    └── dependencies_handling.py
    └── required-libraries.txt
├── account.py
├── combos.py
├── credit.py
├── delivery_window.py
├── discounts_ms.py
├── products.py
├── main.py
```

| Directory | Description |
| ------ | ------ |
| data-mass | All files related to **Data Mass** creation. Includes different files which are used for specific purposes, such as the creation of a new account, and the input of different available product types for each Zone. |

## Important Files

| File | Description |
| ------ | ------ |
| [data-mass/main.py](main.py) | Holds menus and sub-menus for each available operation. It is also used for calling external functions and API requests. |
| [.gitignore](.gitignore) | Holds all files that shouldn't be tracked by system version control. |

## Visual Studio Code plugins

Install the IDE plugins for Visual Studio Code.

> Plugins features and usage reference:

| Plugins |
| ------ |
| [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) |
| [vscode-icons](https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons) |

## Running the Script

To launch the application menu, please follow the steps below after opening the Terminal:

```sh
cd <project-root-dir>/data-mass/
python3 main.py
```
By running this command, anyone will be able to see the application menu, and then choose any of the available options depending on the usage.

## Bug report, feedback & improvement requests

This script was originally developed by the Antarctica Team (Checkout Experience), after they identified that the difficulty and the lack of knowledge for creating data mass for the development and testing were a need for every team involved in this project.

The Quality Management Team has been assigned to take care of this initiative, for both new features to come as well as the maintaince of what has been developed.

If you find any issue, please contact one of following people listed below:

| Developers |
| ------ |
| [Eduardo Oliveira](eduardo.oliveira@ab-inbev.com) - Checkout Experience |
| [José Vieira](jose.vieirajunior@ab-inbev.com) - Quality Management | 
| [Alexandre Rebouças](alexandre.reboucas@ab-inbev.com) Quality Management | 

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GitDoc]: https://git-scm.com/doc
[Python]: https://www.python.org/downloads/
[VisualStudioCode]: https://code.visualstudio.com/download
[Requests]: https://pypi.org/project/requests/
[JSONPath-ext RW]: https://pypi.org/project/jsonpath-rw-ext/
[JSONPath RW]: https://pypi.org/project/jsonpath-rw/