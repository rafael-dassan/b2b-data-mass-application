# B2B Product - Data Mass Script

This repository contains the B2B Data Mass Script, aimed to those who want to create all necessary information to execute tests, develop new features and even explore the apps.

## System Requirements

* Operating system based on UNIX.

## Required Tooling

* [Git][GitDoc]
* [Python 3.5 or higher][Python]

## Directories structure organization

| Directory | Description |
| ------ | ------ |
| data-mass | All files related to **Data Mass** creation. Includes different files which are used for specific purposes, such as the creation of a new account, and the input of different available product types for each Zone. |

## Important Files

| File | Description |
| ------ | ------ |
| [data-mass/main.py](data-mass/main.py) | Holds menus and sub-menus for each available operation. It also executes the script.  |
| [data-mass/common.py](data-mass/common.py) | Holds validation and external functions, and API requests. |
| [.gitignore](.gitignore) | Holds all files that should not be tracked by system version control. |

## Important Notes

### Azure IAM

This script are also capable to create Azure IAM (Identity and Access Management) Users.

One user could be created at a time using Option "Create User IAM" under "Microservice" menu from "main.py" Script.

There's an Integration between Azure and Magento to create a new User in Magento after an Azure IAM User is created. The time to this happen may vary but you should expect to wait around 30 seconds for the synchronization.

At this this time, there's only one Country (DO - Dominican Republic) and two Environments Enabled with IAM Feature:
- DEV for Web
- UAT for Mobile

Here we have a list of fields to create an IAM User:
- A valid E-mail Address - Ex: abiuser@mail.com
- Password - Ex: Magento123
- First Name - Email Prefix - Ex: abiuser
- Last Name - Email Prefix - Ex: abiuser
- Account ID - Ex: 0000248660
- Tax ID - Ex: 00300489572

## Running the Script

To launch the application menu, please follow the steps below after opening the Terminal:

```sh
cd <project-root-dir>/data-mass/
```

You may not have all required dependencies installed by default. Install them by using the pip command:

```sh
pip3 install -r requirements.txt
```

And then you can finally execute the script:

```sh
python3 main.py
```

By running this command, anyone will be able to see the application menu, and then choose any of the available options depending on the usage.

## Additional information

* [Development Standards][Standards]
* [Release Notes][Release Notes]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GitDoc]: https://git-scm.com/doc
[Python]: https://www.python.org/downloads/
[VisualStudioCode]: https://code.visualstudio.com/download
[Requests]: https://pypi.org/project/requests/
[JSONPath-ext RW]: https://pypi.org/project/jsonpath-rw-ext/
[JSONPath RW]: https://pypi.org/project/jsonpath-rw/
[Standards]: https://anheuserbuschinbev.sharepoint.com/sites/b2bengineering/architecture/SitePages/Data-Mass-Application.aspx
[Release Notes]: https://anheuserbuschinbev.sharepoint.com/:b:/s/b2bengineering/EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8
