*** Settings ***

Resource     ${CURDIR}/libraries.robot
Resource     ${CURDIR}/../variables/variables-global.robot
Resource     ${CURDIR}/../keywords/common.robot

Variables    ${CURDIR}/../variables/debug-drawer.py
Variables    ${CURDIR}/../variables/initial-registration-validation-flow.py

*** Keywords ***

I foward to initial registration validation screen
    appium.Click Element                                    id=createAccount
    appium.Wait Until Page Contains                         Create an Account
    std.Sleep                                               2s   
    appium.Capture Page Screenshot

I validate all dialogs contents in initial registration validation screen
    Validate strings on screen                              @{INITAL_REGISTRATION_VALIDATION_SCREEN_TEXTS}
    std.Sleep                                               2s   
    appium.Capture Page Screenshot
    # ${length}                                               std.Get Length                                    ${ELEMENTS_TO_CLICK_LOCATORS}

    # :FOR  ${index}  IN RANGE  ${length}
    # \    @{texts_list}                                      std.Set Variable                                  @{DIALOGS_TEXTS_LIST}[${index}]
    # \    ${element_id}                                      std.Set Variable                                  @{ELEMENTS_TO_CLICK_LOCATORS}[${index}]
    # \    appium.Click Element                               id=${element_id}
    # \    appium.Wait Until Page Contains Element            id=android:id/topPanel
    # \    ${text}                                            appium.Get Text                                   id=android:id/alertTitle
    # \    std.Should Be Equal                                ${text}                                           @{texts_list}[0]                           ignore_case=false
    # \    ${text}                                            appium.Get Text                                   id=android:id/message
    # \    std.Should Be Equal                                ${text}                                           @{texts_list}[1]                           ignore_case=false
    # \    ${text}                                            appium.Get Text                                   id=android:id/button2
    # \    std.Should Be Equal                                ${text}                                           @{texts_list}[2]                           ignore_case=true
    # \    appium.Capture Page Screenshot
    # \    appium.Click Element                               id=android:id/button2
    # \    appium.Wait Until Page Does Not Contain Element    id=android:id/topPanel                            timeout=25s