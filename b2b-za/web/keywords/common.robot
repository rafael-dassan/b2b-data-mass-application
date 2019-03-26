*** Settings ***
Resource    ${CURDIR}/../resources/libraries.robot

*** Keywords ***
Begin Web Test
    selenium.Open Browser     about:blank
    ...                       chrome

End Web Test
    selenium.Close Browser