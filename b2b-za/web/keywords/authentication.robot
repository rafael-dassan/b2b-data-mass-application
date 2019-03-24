*** Settings ***
Resource     ${CURDIR}/../resources/libraries.robot
Resource     ${CURDIR}/../keywords/common.robot
Variables    ${CURDIR}/../variables/authentication.py

*** Keywords ***
I am on the login page
    selenium.Go To                                        https://qa-conv-sabconnect.abi-sandbox.net/customer/account/login/
    selenium.Title Should Be                              Log In

I login with my user credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}

I login with invalid user credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}

I login with empty user credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}

I should be redirected to the home screen
    selenium.Location Should Be                           https://qa-conv-sabconnect.abi-sandbox.net/cms/index/home/
    selenium.Capture Page Screenshot

I should see the invalid credentials error message
    selenium.Page Should Contain Element                  xpath=//*[@id="maincontent"]/div[2]/div[2]/div[1]/div/div
    selenium.Capture Page Screenshot

I should see the empty credentials error messages
    selenium.Page Should Contain Element                  id=email-error
    selenium.Element Text Should Be                       id=email-error
    ...                                                   @{FAIL_REQUIRED_FIELD_TEXT}
    selenium.Page Should Contain Element                  id=pass-error
    selenium.Element Text Should Be                       id=pass-error
    ...                                                   @{FAIL_REQUIRED_FIELD_TEXT}
    selenium.Capture Page Screenshot

Input Login Credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    selenium.Clear Element Text                           id=email
    selenium.Input Text                                   id=email
    ...                                                   ${user_email}
    selenium.Clear Element Text                           id=pass
    selenium.Input Text                                   id=pass
    ...                                                   ${user_password}
    selenium.Click Button                                 xpath=//*[@id="send2"]

Unsucessful Login Invalid Credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    I am on the login page
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}
    I should see the invalid credentials error message

Unsucessful Login Empty Credentials
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    I am on the login page
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}

    std.Run Keyword If                                    '${user_email}' == '${EMPTY}' and '${user_password}' != '${EMPTY}'
    ...                                                   selenium.Element Text Should Be
    ...                                                   id=email-error
    ...                                                   @{FAIL_REQUIRED_FIELD_TEXT}
    ...                                                   ELSE IF
    ...                                                   '${user_password}' == '${EMPTY}' and '${user_email}' != '${EMPTY}'
    ...                                                   selenium.Element Text Should Be
    ...                                                   id=pass-error
    ...                                                   @{FAIL_REQUIRED_FIELD_TEXT}
    selenium.Capture Page Screenshot

Unsucessful Login Invalid Email Format
    [Arguments]                                           ${user_email}
    ...                                                   ${user_password}
    I am on the login page
    Input Login Credentials                               ${user_email}
    ...                                                   ${user_password}
    selenium.Page Should Contain Element                  id=email-error
    selenium.Element Text Should Be                       id=email-error
    ...                                                   @{FAIL_INVALID_EMAIL_FORMAT_TEXT}
    selenium.Capture Page Screenshot