*** Settings ***
Resource     ${CURDIR}/../page-objects/LoginPage.robot
Resource     ${CURDIR}/../page-objects/HomePage.robot
Resource     ${CURDIR}/../keywords/common.robot
Variables    ${CURDIR}/../variables/authentication.py

*** Keywords ***
I am on the login page
    LoginPage.Load Page
    LoginPage.Verify Page Loaded

I login with my user credentials
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}

I login with invalid user credentials
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}

I login with empty user credentials
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}

Log in as a regular user
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    I am on the login page
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}
    I should be redirected to the home screen

I should be redirected to the home screen
    HomePage.Verify Page Loaded

I should see the invalid credentials error message
    LoginPage.Validate Invalid Credentials Error Message

I should see the empty credentials error messages
    LoginPage.Validate Empty Credentials Error Messages

Unsucessful Login Invalid Credentials
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    I am on the login page
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}
    I should see the invalid credentials error message

Unsucessful Login Empty Credentials
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    I am on the login page
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}

    std.Run Keyword If                                      '${user_email}' == '${EMPTY}' and '${user_password}' != '${EMPTY}'
    ...                                                     Validate Empty Email Error Message
    ...                                                     ELSE IF
    ...                                                     '${user_password}' == '${EMPTY}' and '${user_email}' != '${EMPTY}'
    ...                                                     Validate Empty Password Error Message
    selenium.Capture Page Screenshot

Unsucessful Login Invalid Email Format
    [Arguments]                                             ${user_email}
    ...                                                     ${user_password}
    I am on the login page
    LoginPage.Input Login Credentials                       ${user_email}
    ...                                                     ${user_password}
    LoginPage.Validate Invalid Email Format Message