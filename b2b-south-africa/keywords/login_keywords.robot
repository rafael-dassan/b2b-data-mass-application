*** Keywords ***

A login error message is displayed
  appium.Wait Until Page Contains Element           ${TP_LOGIN_ERROR_MESSAGE}  ${TIMEOUT}
  ${errorMessage}                                   appium.Get Text  ${TV_LOGIN_ERROR_MESSAGE}
  @{listErrorMessages}                              std.Create List  ${UNSUCCESSFUL_AUTHENTICATION_INVALID_USER_MESSAGE}  ${UNSUCCESSFUL_AUTHENTICATION_INVALID_PASSSWORD_MESSAGE}
  std.Should Contain Any                            ${errorMessage}  @{listErrorMessages}  ignore_case=false
  ${confirmButtonText}                              appium.Get Text  ${BTN_LOGIN_CONFIRM}
  std.Should Be Equal                               ${confirmButtonText}  ${UNSUCCESSFUL_AUTHENTICATION_DIALOG_BUTTON_MESSAGE}  ignore_case=true
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/login_error_message.png
  appium.Click Element                              ${BTN_LOGIN_CONFIRM}
  appium.Wait Until Page Does Not Contain Element   ${TP_LOGIN_ERROR_MESSAGE}  ${TIMEOUT}

I login with invalid password
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/invalid_password.png
  appium.Click Element                              ${BTN_LOGIN}

The Login button must be disabled
  appium.Element Should Be Disabled                 ${BTN_LOGIN}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/login_button_disabled.png

I login with invalid email
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/invalid_email.png
  appium.Click Element                              ${BTN_LOGIN}

I do not enter the login credentials
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/empty_credentials.png
  appium.Click Element                              ${BTN_LOGIN}

I choose the POC
  [Arguments]                                       ${poc}
  appium.Wait Until Page Contains Element           ${ACCOUNT_VIEW}  ${TIMEOUT}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/chosen_poc.png
  appium.Click Text                                 ${poc}

I login with my user credentials
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/valid_credentials.png
  appium.Click Element                              ${BTN_LOGIN}