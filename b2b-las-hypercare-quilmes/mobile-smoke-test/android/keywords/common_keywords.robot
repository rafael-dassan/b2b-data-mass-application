*** Keywords ***

Open App
  appium.Open Application                         ${GLOBAL_APPIUM_SERVER_ADDRESS}   
  ...                                             platformName=${GLOBAL_PLATFORM_NAME}   
  ...                                             platformVersion=${GLOBAL_PLATFORM_VERSION}   
  ...                                             deviceName=${GLOBAL_DEVICE_NAME}  
  ...                                             appPackage=${GLOBAL_APP_PACKAGE}   
  ...                                             appActivity=${GLOBAL_APP_ACTIVITY}   
  ...                                             automationName=${GLOBAL_AUTOMATION_NAME}    
  ...                                             app=${GLOBAL_APPLICATION_APK}    
  ...                                             noReset=false    
  ...                                             fullReset=false      
  ...                                             newCommandTimeout=0        
  ...                                             adbExecTimeout=86400       
  ...                                             waitAction=350      
  ...                                             printPageSourceOnFindFailure=true       
  ...                                             deviceReadyTimeout=15       
  ...                                             avd=${GLOBAL_AVD}

Bootstrap test environment
  ${command}                                      std.Set Variable  adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done
  process.Run Process                             ${command}  shell=true
  ${command}                                      std.Set Variable  %{ANDROID_HOME}/emulator/emulator -avd ${GLOBAL_AVD} &
  process.Run Process                             ${command}  shell=true  stdout=/dev/null  stderr=/dev/null
  std.Sleep                                       ${BOOTSTRAP_SLEEP}
  ${command}                                      std.Set Variable  ps -ef | grep appium | grep -v grep | awk '{print $2}' | xargs kill -9
  std.Log                                         ${command}  console=true
  process.Run Process                             ${command}  shell=true
  ${command}                                      std.Set Variable  appium --session-override --reboot &
  std.Log                                         ${command}  console=true
  process.Run Process                             ${command}  shell=true  stdout=/dev/null  stderr=/dev/null
  std.Sleep                                       ${BOOTSTRAP_SLEEP}
  Open App

Swipe From Right To Left
  appium.Swipe By Percent                         95  50	05  50  350

Show Debug Drawer
  appium.Swipe By Percent                         98  50	15	50  350

Hide Debug Drawer
  appium.Swipe By Percent                         50  50	99	50  350

I select the environment
  [Arguments]                                     ${environment}
  collections.List Should Contain Value           ${GLOBAL_ENVIRONMENTS}  ${environment} 
  std.Log                                         \nRunning tests against ${environment}  console=yes
  appium.Wait Until Page Contains Element         ${BTN_GO_TO_LOGIN}  ${TIMEOUT}
  appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/home/home_screen.png
  Show Debug Drawer
  appium.Click Text                               ${environment}
  appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/home/environment_selection.png
  Hide Debug Drawer

I navigate through all introduction screens
  :FOR  ${index}  IN RANGE  ${TOTAL_TUTORIAL_SCREENS}
  \    ${tutorial_screen_number}                  std.Evaluate  ${index} + 1
  \    ${is_not_last_tutorial_screen}             std.Evaluate  ${tutorial_screen_number} < ${TOTAL_TUTORIAL_SCREENS}
  \    appium.Wait Until Page Contains Element    ${TUTORIAL_IMAGE}  ${TIMEOUT}
  \    appium.Capture Page Screenshot             ${LOGDIR}/screenshots/tutorial/tutorial_page_${index}.png
  \    std.Run Keyword If                         ${is_not_last_tutorial_screen}  Swipe From Right To Left

  # When in last tutorial screen
  appium.Page Should Contain Element              ${BTN_TUTORIAL_START}
  appium.Click Element                            ${BTN_TUTORIAL_START}

I will be redirected to browse screen
  appium.Wait Until Page Contains Element         ${BROWSE_VIEW}  ${TIMEOUT}
  std.Sleep                                       ${SCREENSHOT_SLEEP}
  appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/browse/browse_screen.png

I have logged into the application
  I select the environment                        ${TEST_ENVIRONMENT}
  I login with my user credentials                ${VALID_USER_MORE_POCS}  ${VALID_PASS_MORE_POCS}
	I choose the POC						                    ${TEST_POC}
  I navigate through all introduction screens
  I will be redirected to browse screen

Go to the menu
  appium.Wait Until Page Contains Element         ${HAMBURGUER_MENU}  ${TIMEOUT}
  appium.Click Element                            ${HAMBURGUER_MENU}
  
Close App
  appium.Close Application
  process.Run Process                             ${KILL_EMULATOR_COMMAND}  shell=true

#======================================== LOGIN ========================================#
A login error message is displayed
  appium.Wait Until Page Contains Element           ${TP_LOGIN_ERROR_MESSAGE}  ${TIMEOUT}
  ${errorMessage}                                   appium.Get Text  ${TV_LOGIN_ERROR_MESSAGE}
  std.Should Contain Any                            ${errorMessage}  @{LOGIN_INVALID_MESSAGE}  ignore_case=false
  appium.Element Should Contain Text                ${BTN_LOGIN_CONFIRM}  ${LOGIN_DIALOG_BTN_MESSAGE}  ${TIMEOUT}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/login_error_message.png
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
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/invalid_password.png
  appium.Click Element                              ${BTN_LOGIN}

The Login button must be disabled
  appium.Element Should Be Disabled                 ${BTN_LOGIN}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/login_button_disabled.png

I login with invalid email
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/invalid_email.png
  appium.Click Element                              ${BTN_LOGIN}

I do not enter the login credentials
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/empty_credentials.png
  appium.Click Element                              ${BTN_LOGIN}

I choose the POC
  [Arguments]                                       ${poc}
  appium.Wait Until Page Contains Element           ${ACCOUNT_VIEW}  ${TIMEOUT}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/chosen_poc.png
  appium.Click Text                                 ${poc}

I login with my user credentials
  [Arguments]                                       ${user}  ${password}
  std.Log                                           \nUser credentials: ${user} \nPassword: ${password}  console=yes
  appium.Click Element                              ${BTN_GO_TO_LOGIN}
  appium.Wait Until Page Contains Element           ${LOGIN_FORM}  ${TIMEOUT}                                              
  appium.Input Text                                 ${ET_USERNAME}  ${user}
  appium.Input Password                             ${ET_PASSWORD}  ${password}
  std.Sleep                                         ${SCREENSHOT_SLEEP}
  appium.Capture Page Screenshot                    ${LOGDIR}/screenshots/login/valid_credentials.png
  appium.Click Element                              ${BTN_LOGIN}