# B2B Data Mass Script
This repository contains the B2B Data Mass Script, aimed to those who want to create all necessary information to execute tests, develop new features and even explore the apps.

[Lengua española readme](doc/README.es.md) • [Readme português](doc/README.p.md)

## System Requirements
* Operating system based on UNIX.

## Required Tooling
*  [Git][GitDoc]
*  [Python 3.7 or higher][Python]

## Setting Up the Environment
To maintain a pure and error-free Python environment for running Data Mass, follow the steps below:

### Using script
Change the permissions of the script:
```bash
chmod +x env-maker.sh
```

Run the script:
```bash
./env-maker.sh
```

Activate the virtualenv:
```bash
source venv/bin/activate
```

### Manually
Follow the [virtualenv installation guide](doc/USER_GUIDE.md#using-virtualenv).

## Installing the Application
After enabling the virtualenv, install the application:
```sh
python3 setup.py install
```

To use development mode*:
```sh
python3 setup.py install develop
```

\* [More detail can be found in the official documentation](https://setuptools.readthedocs.io/en/latest/userguide/development_mode.html).

## Running the Application
To start the application, run:
```sh
python3 -m data_mass.main
```

By running this command, anyone will be able to see the application menu, and then choose any of the available options depending on the usage.

## Contributing to Data Mass
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](doc/USER_GUIDE.md#contributing-to-data-mass).

Check out our [code style guide](doc/C_STYLE_GUIDE.md) (available in english only)!

## Additional Information
*  [Development Standards][Standards]
*  [Release Notes][Release Notes]

[//]: #  (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[GitDoc]: https://git-scm.com/doc
[Python]: https://www.python.org/downloads/
[Standards]: https://anheuserbuschinbev.sharepoint.com/sites/b2bengineering/architecture/SitePages/Data-Mass-Application.aspx
[Release Notes]: https://anheuserbuschinbev.sharepoint.com/:b:/s/b2bengineering/EaTlUWEzsp1EqdmKaqBclL4ByT6uvxDV1nF1erEOsD-stQ?e=QQyxU8
