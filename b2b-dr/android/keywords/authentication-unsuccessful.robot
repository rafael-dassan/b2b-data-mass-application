*** Settings ***

Resource     ${CURDIR}/libraries.robot
Resource     ${CURDIR}/../variables/variables-global.robot
Resource     ${CURDIR}/../keywords/common.robot

Variables    ${CURDIR}/../variables/debug-drawer.py
Variables    ${CURDIR}/../variables/authentication-flow.py

*** Keywords ***


Unsuccessful login
    [Arguments]                                        ${user}                  
    ...                                                ${password}
    appium.Clear Text                                  id=username
    appium.Input Text                                  id=username               
    ...                                                ${user}
    appium.Clear Text                                  id=newPassword
    appium.Input Password                              id=newPassword            
    ...                                                ${password}
    std.Sleep                                          time_=100ms
    appium.Capture Page Screenshot
    appium.Click Element                               id=login
    appium.Wait Until Page Contains Element            id=android:id/topPanel    
    ...                                                timeout=60s
    appium.Capture Page Screenshot
    ${error_message}                                   appium.Get Text           
    ...                                                id=android:id/message
    @{items}                                           std.Create List           
    ...                                                ${UNSUCCESSFUL_AUTHENTICATION_INVALID_USER_MESSAGE}     
    ...                                                ${UNSUCCESSFUL_AUTHENTICATION_INVALID_PASSSWORD_MESSAGE}
    std.Should Contain Any                             ${error_message}          
    ...                                                @{items}                                                
    ...                                                ignore_case=false
    ${confirm_button_text}                             appium.Get Text           
    ...                                                id=android:id/button2
    std.Should Be Equal                                ${confirm_button_text}    
    ...                                                ${UNSUCCESSFUL_AUTHENTICATION_DIALOG_BUTTON_MESSAGE}    
    ...                                                ignore_case=true
    appium.Click Element                               id=android:id/button2
    appium.Wait Until Page Does Not Contain Element    id=android:id/topPanel    timeout=60s


Login action disabled
    [Arguments]                                        ${user}                   ${password}
    appium.Clear Text                                  id=username
    appium.Input Text                                  id=username               ${user}
    appium.Clear Text                                  id=newPassword
    appium.Input Password                              id=newPassword            ${password}
    std.Sleep                                          time_=100ms
    appium.Capture Page Screenshot
    appium.Element Should Be Disabled                  id=login

Invalid user
    [Arguments]                                        ${user}                   ${password}
    Unsuccessful login                                 ${user}                   ${password}

Invalid password
    [Arguments]                                        ${user}                   ${password}
    Unsuccessful login                                 ${user}                   ${password}
