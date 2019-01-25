*** Settings ***

# Keywords
Resource    ${CURDIR}/../keywords/common_keywords.robot
Resource    ${CURDIR}/../keywords/login_keywords.robot

# Variables
Resource    ${CURDIR}/../variables/global_variables.robot
Resource    ${CURDIR}/../variables/login_variables.robot

# Python files
Variables   ${CURDIR}/../variables/messages.py

# Library aliases
Library     AppiumLibrary    WITH NAME  appium
Library     BuiltIn          WITH NAME  std
Library     Collections      WITH NAME  collections
Library     Process          WITH NAME  process
Library     OperatingSystem  WITH NAME  operatingsystem
Library     DateTime         WITH NAME  datetime
Library     String           WITH NAME  str