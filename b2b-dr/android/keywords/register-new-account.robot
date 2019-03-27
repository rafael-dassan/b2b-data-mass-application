*** Settings ***

Resource     ${CURDIR}/libraries.robot
Resource     ${CURDIR}/../variables/variables-global.robot
Resource     ${CURDIR}/../keywords/common.robot
Variables    ${CURDIR}/../variables/debug-drawer.py
Variables    ${CURDIR}/../variables/register-new-account-flow.py


*** Keywords ***
I go to the register screen

    appium.Click Element                       id=createAccount
    appium.Wait Until Page Contains Element    id=nextButton
    ...                                        timeout=20s

I input personal information
    [Arguments]                                ${firstName}
    ...                                        ${lastName}

    appium.Input Value                         id=firstName
    ...                                        ${firstName}
    appium.Input Text                          id=lastName
    ...                                        ${lastName}

I input an email address that has never been used before
    ${temp}                                    faker.Free Email
    std.Set Suite Variable                     ${email}
    ...                                        ${temp}

    appium.Input Text                          id=emailAddress
    ...                                        ${email}

I input confirmation email address
    ${emailConfirmationAddress}                std.Set Variable
    ...                                        ${email}
    appium.Input Text                          id=emailConfirmationAddress
    ...                                        ${emailConfirmationAddress}


I input email invalid
    [Arguments]                                ${email}
    ...                                        ${emailConfirmationAddress}
    appium.Input Text                          id=emailAddress
    ...                                        ${email}
    appium.Input Text                          id=emailConfirmationAddress
    ...                                        ${emailConfirmationAddress}

I input email already registered before
    [Arguments]                                ${email}
    ...                                        ${emailConfirmationAddress}
    appium.Input Text                          id=emailAddress
    ...                                        ${email}
    appium.Input Text                          id=emailConfirmationAddress
    ...                                        ${emailConfirmationAddress}

I input a Cell Phone Number
    [Arguments]                                ${phoneNumber}
    appium.Input Text                          id=phoneNumber
    ...                                        ${phoneNumber}
    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot

I go to the next registration step 1
    appium.Click Element                       id=nextButton
    appium.Wait Until Page Contains Element    id=nextButton
    ...                                        timeout=20s

I input my account
    [Arguments]                                ${customerId}
    ...                                        ${liquorLicenceNumber}

    appium.Input Value                         id=customerId
    ...                                        ${customerId}
    appium.Input Text                          id=liquorLicenceNumber
    ...                                        ${liquorLicenceNumber}

    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot

I not input my account
    [Arguments]                                ${customerId}
    ...                                        ${liquorLicenceNumber}

    appium.Input Value                         id=customerId
    ...                                        ${customerId}
    appium.Input Text                          id=liquorLicenceNumber
    ...                                        ${liquorLicenceNumber}

    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot

I go to the next registration step 2
    appium.Click Element                       id=nextButton
    appium.Wait Until Page Contains Element    id=soundsGoodBtn
    ...                                        timeout=20s

    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot

I confirm that I want to register
    Validate strings on screen                 @{ACCOUNT_CONFIRMATION_SCREEN_TEXTS}
    appium.Capture Page Screenshot
    appium.Click Element                       id=soundsGoodBtn
    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot

I my account should not have been created
    appium.Click Element                       id=soundsGoodBtn
    appium.Capture Page Screenshot
    appium.Wait Until Page Contains Element    id=android:id/button2
    ...                                        timeout=20s
    Validate strings on screen                 @{FAIL_ACCOUNT_CONFIRMATION_DIALOG_TEXTS}
    std.Sleep                                  time_=2s
    appium.Capture Page Screenshot
    appium.Click Element                       id=android:id/button2
    appium.Capture Page Screenshot

I click in ok button next invalid
    appium.Click Element                       id=nextButton
    appium.Capture Page Screenshot

I confirm email invalid
    appium.Click Element                       id=nextButton
    appium.Capture Page Screenshot

I try to advance to my account data screen
    Validate strings on screen                 @{FAIL_E_MAIL_DIALOG_TEXTS}
    appium.Capture Page Screenshot

I try to advance to my account data screen error confirmation
    Validate strings on screen                 @{FAIL_E_MAIL_CONFIRMATION_DIALOG_TEXTS}
    appium.Capture Page Screenshot

