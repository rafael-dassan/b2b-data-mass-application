*** Settings ***
Resource     ${CURDIR}/../resources/libraries.robot

*** Keywords ***
Begin Web Test
    Open Browser       about:blank     chrome

End Web Test
    Close Browser