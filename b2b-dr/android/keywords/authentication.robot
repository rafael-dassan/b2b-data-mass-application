*** Settings ***

Resource     ${CURDIR}/libraries.robot
Resource     ${CURDIR}/../variables/variables-global.robot
Resource     ${CURDIR}/../keywords/common.robot

Variables    ${CURDIR}/../variables/debug-drawer.py
Variables    ${CURDIR}/../variables/authentication-flow.py

*** Keywords ***

I login with my user credentials
    [Arguments]                                     ${user}                                  ${password}
    Validate strings on screen                      @{STARTUP_SCREEN_TEXTS}
    appium.Click Element                            id=logIn
    appium.Wait Until Page Contains Element         id=signInForm                            timeout=20s
    Validate strings on screen                      @{AUTHENTICATION_SCREEN_TEXTS}
    appium.Input Text                               id=username                              ${user}
    appium.Input Password                           id=newPassword                           ${password}
    std.Sleep                                       time_=100ms
    appium.Capture Page Screenshot
    appium.Click Element                            id=login

I navigate through all introduction screens
    ${length}                                       std.Get Length                           ${TUTORIAL_SCREENS_TEXTS_LIST}

    :FOR  ${index}  IN RANGE  ${length}
    \    @{texts_list}                              std.Set Variable                         @{TUTORIAL_SCREENS_TEXTS_LIST}[${index}]
    \    ${tutorial_screen_number}                  std.Evaluate                             ${index} + 1
    \    ${is_not_last_tutorial_screen}             std.Evaluate                             ${tutorial_screen_number} < ${length}
    \    appium.Wait Until Page Contains Element    id=tutorial_image                        timeout=60s
    \    Validate strings on screen                 @{texts_list}
    \    appium.Capture Page Screenshot
    \    std.Run Keyword If                         ${is_not_last_tutorial_screen}           Swipe From Right To Left

    # When in last tutorial screen
    appium.Page Should Contain Element              id=start_button
    appium.Click Element                            id=start_button

I will be redirected to browse screen
    appium.Wait Until Page Contains Element         id=browse_recyclerview                   timeout=60s
    std.Sleep                                       time_=100ms
    appium.Capture Page Screenshot

I choose the POC
    [Arguments]                                     ${poc}
    appium.Wait Until Page Contains Element         id=account_recyclerview                  timeout=60s
    Validate strings on screen                      @{POC_SELECTION_SCREEN_TEXTS}
    std.Sleep                                       time_=100ms
    appium.Capture Page Screenshot
    appium.Click Text                               text=${poc}

I go from startup screen to authentication screen
    [Arguments]                                     ${user}                                  ${password}
    appium.Capture Page Screenshot
    appium.Click Element                            id=logIn
    appium.Wait Until Page Contains Element         id=signInForm                            timeout=20s

I click to contact the customer service through phone
    appium.Capture Page Screenshot
    appium.Wait Until Page Contains Element         id=help_phone                            timeout=20s
    appium.Click Element                            id=help_phone

I see the phone application is opened
    appium.Capture Page Screenshot
    appium.Wait Until Page Contains Element         id=com.android.dialer:id/dialpad_view
    appium.Page Should Contain Text                 ${VALIDATE_PHONE_TEXTS}

I click to contact the customer service through e-mail
    appium.Capture Page Screenshot
    appium.Wait Until Page Contains Element         id=helpEmail                             timeout=20s
    appium.Click Element                            id=helpEmail

I see the e-mail application is opened
    appium.Wait Until Page Contains Element         id=android:id/resolver_list
    appium.Capture Page Screenshot
    appium.Click Text                               ${SELECT_EMAIL_TEXTS}
    appium.Wait Until Page Contains Element         id=com.google.android.gm:id/subject
    appium.Page Should Contain Text         ${VALIDATE_EMAIL_SUBJECT_TEXTS}
    appium.Capture Page Screenshot
