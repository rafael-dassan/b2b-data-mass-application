# B2B Product Acceptance Tests Automatization

## System Requirements

* Operating system based on UNIX.

## Required Tooling

* [Git][GitDoc]

## Directories Structure Organization

```sh
exmaple/
├── a
├── b
│   └── b1
├── c
└── d
    └── d1
    └── d2
```
## Description

* This folder will contain all utilitary scripts used to support the testing routines of the BeerTech team.

## Scripts details

| Script | Description |
| ------ | ------ |
| monkey_test.sh | This script executes a monkey test in the connected device. It only requires one parameter, which is the package of the application that is going to be tested. After finishing, if there are any crashes, it will generate a .txt file that contains evidences about the failure. **It is highly recommended that the tester log into the application and only then start the test. This is important because it will prevent the monkeys from getting stuck in the login screen.** |