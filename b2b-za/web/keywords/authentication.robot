*** Settings ***
Resource     ${CURDIR}/../resources/libraries.robot

*** Keywords ***
I am on the login page
    selenium.Go To   ${WEB_LOGIN_URL}
    selenium.Title Should Be    Log In

I login with my user credentials
    [Arguments]     ${user_email}   ${user_password}
    selenium.Clear Element Text     id=email
    selenium.Input Text             id=email       ${user_email}
    selenium.Clear Element Text     id=pass
    selenium.Input Text             id=pass        ${user_password}
    selenium.Click Button           xpath=//*[@id="send2"]

I should be redirected to the home screen
    selenium.Location Should Be     https://qa-conv-sabconnect.abi-sandbox.net/cms/index/home/






