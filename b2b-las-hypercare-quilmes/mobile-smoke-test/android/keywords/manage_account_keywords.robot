*** Keywords ***

I change my password
    [Arguments]                                         ${current_password}  ${new_password}  ${new_password_match}
    Go to the menu
    appium.Wait Until Page Contains Element             ${TV_CUSTOMER_ID}  ${TIMEOUT}
    appium.Page Should Contain Text                     ${MENU_SETTINGS_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/browse/application_menu.png
    appium.Click Text                                   ${MENU_SETTINGS_MESSAGE}
    appium.Wait Until Page Contains Element             ${CHANGE_PASSWORD_CELL}  ${TIMEOUT}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/settings_screen.png
    appium.Click Element                                ${CHANGE_PASSWORD_CELL}
    appium.Wait Until Page Contains Element             ${ET_CURRENT_PASSWORD}  ${TIMEOUT}
    appium.Input Password                               ${ET_CURRENT_PASSWORD}  ${current_password}
    appium.Input Password                               ${ET_NEW_PASSWORD}  ${new_password}
    appium.Input Password                               ${ET_CONFIRM_NEW_PASSWORD}  ${new_password_match}

I do not enter the passwords
    [Arguments]                                         ${current_password}  ${new_password}  ${new_password_match}
    I change my password                                ${current_password}  ${new_password}  ${new_password_match} 

I enter different passwords
    [Arguments]                                         ${current_password}  ${new_password}  ${new_password_match}
    I change my password                                ${current_password}  ${new_password}  ${new_password_match}

I enter wrong current password
    [Arguments]                                         ${current_password}  ${new_password}  ${new_password_match}
    I change my password                                ${current_password}  ${new_password}  ${new_password_match}

I enter a password with invalid format
    [Arguments]                                         ${current_password}  ${new_password}  ${new_password_match}
    I change my password                                ${current_password}  ${new_password}  ${new_password_match}

I must receive a password invalid format error message
    appium.Click Element                                ${BTN_PASSWORD_CHANGE}
    appium.Wait Until Page Contains Element             ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_PASSWORD_CHANGE}  ${PASSWORD_CHANGE_INVALID_MESSAGE}
    appium.Element Should Contain Text                  ${BTN_PASSWORD_CHANGE_DIALOG}  ${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/password_invalid_format_error_message.png
    appium.Click Element                                ${BTN_PASSWORD_CHANGE_DIALOG}
    appium.Wait Until Page Does Not Contain Element     ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT} 

I must receive a password minimum length error message
    appium.Click Element                                ${BTN_PASSWORD_CHANGE}
    appium.Wait Until Page Contains Element             ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_PASSWORD_CHANGE}  ${PASSWORD_CHANGE_MINIMUM_LENGTH_MESSAGE}
    appium.Element Should Contain Text                  ${BTN_PASSWORD_CHANGE_DIALOG}  ${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/password_minimum_length_error_message.png
    appium.Click Element                                ${BTN_PASSWORD_CHANGE_DIALOG}
    appium.Wait Until Page Does Not Contain Element     ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT} 

I must receive a wrong current password error message
    appium.Click Element                                ${BTN_PASSWORD_CHANGE}
    appium.Wait Until Page Contains Element             ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_PASSWORD_CHANGE}  ${INVALID_CURRENT_PASSWORD_MESSAGE}
    appium.Element Should Contain Text                  ${BTN_PASSWORD_CHANGE_DIALOG}  ${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/wrong_current_password_error_message.png
    appium.Click Element                                ${BTN_PASSWORD_CHANGE_DIALOG}
    appium.Wait Until Page Does Not Contain Element     ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT} 

I must receive a password match error message
    appium.Click Element                                ${BTN_PASSWORD_CHANGE}
    appium.Wait Until Page Contains Element             ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_PASSWORD_CHANGE}  ${PASSWORD_NOT_MATCHING_MESSAGE}
    appium.Element Should Contain Text                  ${BTN_PASSWORD_CHANGE_DIALOG}  ${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/password_match_error_message.png
    appium.Click Element                                ${BTN_PASSWORD_CHANGE_DIALOG}
    appium.Wait Until Page Does Not Contain Element     ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}        

The Change Password button must be disabled
    appium.Element Should Be Disabled                   ${BTN_PASSWORD_CHANGE}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/change_password_button_disabled.png

The password must be changed successfully
    appium.Click Element                                ${BTN_PASSWORD_CHANGE}
    appium.Wait Until Page Contains Element             ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_PASSWORD_CHANGE}  ${PASSWORD_CHANGE_SUCESSFULL_MESSAGE}     
    appium.Element Should Contain Text                  ${BTN_PASSWORD_CHANGE_DIALOG}  ${PASSWORD_CHANGE_CONFIRM_DIALOG_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/settings/password_change_sucessfully_message.png
    appium.Click Element                                ${BTN_PASSWORD_CHANGE_DIALOG}
    appium.Wait Until Page Does Not Contain Element     ${TP_PASSWORD_CHANGE_DIALOG}  ${TIMEOUT}

I switch my account
    Go to the menu
    appium.Wait Until Page Contains Element             ${CHANGE_ACCOUNT_DROPDOWN}  ${TIMEOUT}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/account/application_menu_switch_account.png
    appium.Click Element                                ${CHANGE_ACCOUNT_DROPDOWN}
    appium.Wait Until Page Contains Element             ${POCS_TO_CHOOSE}  ${TIMEOUT}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/account/pocs_to_be_chosen.png
    appium.Click Text                                   ${POC_SWITCH_ACCOUNT}

I must be redirected to the other account
    Go to the menu
    appium.Wait Until Page Contains Element             ${TV_CUSTOMER_ID}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_CUSTOMER_ID}  ${POC_NUMBER_SWITCH_ACCOUNT}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/account/switch_account_successfully.png