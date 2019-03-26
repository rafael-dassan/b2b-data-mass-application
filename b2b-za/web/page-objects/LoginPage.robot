*** Settings ***
Resource                       ${CURDIR}/../resources/libraries.robot

*** Variable ***
${LOGINPAGE_URL}               https://qa-conv-sabconnect.abi-sandbox.net/customer/account/login/
${LOGINPAGE_INPUT_EMAIL}       id=email
${LOGINPAGE_INPUT_PASS}        id=pass
${LOGIN_PAGE_SUBMIT_BUTTON}    xpath=//*[@id="send2"]
${LOGINPAGE_ERROR_MODAL}       xpath=//*[@id="maincontent"]/div[2]/div[2]/div[1]/div/div
${LOGINPAGE_EMAIL_ERROR}       id=email-error
${LOGINPAGE_PASS_ERROR}        id=pass-error
${LOGINPAGE_HEADER}            xpath=//*[@id="maincontent"]/div[1]/h1/span

*** Keywords ***
Load Page
    selenium.Go To                          ${LOGINPAGE_URL}

Verify Page Loaded
    selenium.Page Should Contain Element    ${LOGINPAGE_HEADER}

Input Login Credentials
    [Arguments]                             ${user_email}
    ...                                     ${user_password}
    selenium.Clear Element Text             ${LOGINPAGE_INPUT_EMAIL}
    selenium.Input Text                     ${LOGINPAGE_INPUT_EMAIL}
    ...                                     ${user_email}
    selenium.Clear Element Text             ${LOGINPAGE_INPUT_PASS}
    selenium.Input Text                     ${LOGINPAGE_INPUT_PASS}
    ...                                     ${user_password}
    selenium.Click Button                   ${LOGIN_PAGE_SUBMIT_BUTTON}

Validate Invalid Credentials Error Message
    selenium.Page Should Contain Element    ${LOGINPAGE_ERROR_MODAL}
    selenium.Capture Page Screenshot

Validate Empty Credentials Error Messages
    selenium.Page Should Contain Element    ${LOGINPAGE_EMAIL_ERROR}
    selenium.Element Text Should Be         ${LOGINPAGE_EMAIL_ERROR}
    ...                                     @{FAIL_REQUIRED_FIELD_TEXT}
    selenium.Page Should Contain Element    ${LOGINPAGE_PASS_ERROR}
    selenium.Element Text Should Be         ${LOGINPAGE_PASS_ERROR}
    ...                                     @{FAIL_REQUIRED_FIELD_TEXT}
    selenium.Capture Page Screenshot

Validate Empty Email Error Message
    selenium.Element Text Should Be         ${LOGINPAGE_EMAIL_ERROR}
    ...                                     @{FAIL_REQUIRED_FIELD_TEXT}

Validate Empty Password Error Message
    selenium.Element Text Should Be         ${LOGINPAGE_PASS_ERROR}
    ...                                     @{FAIL_REQUIRED_FIELD_TEXT}

Validate Invalid Email Format Message
    selenium.Page Should Contain Element    ${LOGINPAGE_EMAIL_ERROR}
    selenium.Element Text Should Be         ${LOGINPAGE_EMAIL_ERROR}
    ...                                     @{FAIL_INVALID_EMAIL_FORMAT_TEXT}
    selenium.Capture Page Screenshot