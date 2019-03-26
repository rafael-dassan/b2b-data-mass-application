*** Settings ***
Resource           ${CURDIR}/../resources/libraries.robot

*** Variable ***
${HOMEPAGE_URL}    https://qa-conv-sabconnect.abi-sandbox.net/cms/index/home/

*** Keywords ***
Verify Page Loaded
    selenium.Location Should Be         ${HOMEPAGE_URL}
    selenium.Capture Page Screenshot