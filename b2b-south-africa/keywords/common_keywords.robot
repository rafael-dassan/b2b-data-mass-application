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
  Shutdown android virtual device
  #Shutdown appium server
  Start android virtual device
  std.Sleep                                       ${BOOTSTRAP_SLEEP}
  #Start appium server
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
  std.Log                                         \nRunning tests against: ${environment}  console=yes
  appium.Wait Until Page Contains Element         ${BTN_GO_TO_LOGIN}  ${TIMEOUT}
  #appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/home/home_screen.png
  Show Debug Drawer
  appium.Click Text                               ${environment}
  #appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/home/environment_selection.png
  Hide Debug Drawer
  Validate landing screen

I navigate through all introduction screens
  ${length}                                       std.Get Length                    ${TUTORIAL_SCREENS_TEXTS_LIST}

  :FOR  ${index}  IN RANGE  ${length}
  \    @{listTexts}                               std.Set Variable  @{TUTORIAL_SCREENS_TEXTS_LIST}[${index}]
  \    ${tutorial_screen_number}                  std.Evaluate  ${index} + 1
  \    ${is_not_last_tutorial_screen}             std.Evaluate  ${tutorial_screen_number} < ${length}
  \    appium.Wait Until Page Contains Element    ${TUTORIAL_IMAGE}  ${TIMEOUT}
  \    Validate strings on screen                 @{listTexts}
  #\    appium.Capture Page Screenshot             ${LOGDIR}/screenshots/tutorial/tutorial_page_${index}.png
  \    std.Run Keyword If                         ${is_not_last_tutorial_screen}  Swipe From Right To Left

  # When in last tutorial screen
  appium.Page Should Contain Element              ${BTN_TUTORIAL_START}
  ${startButtonText}                              appium.Get Text  ${BTN_TUTORIAL_START} 
  std.Should Be Equal                             ${startButtonText}  ${TUTORIAL_START_BUTTON_TEXT}  ignore_case=true
  appium.Click Element                            ${BTN_TUTORIAL_START}

I will be redirected to browse screen
  ${length}                                       std.Get Length   ${BROWSE_SCREEN_TEXTS}
  appium.Wait Until Page Contains Element         ${BROWSE_VIEW}  ${TIMEOUT}
  ${get_company_name}                             appium.Get Text   ${TV_COMPANY_NAME}
  std.Should Contain Any                          ${get_company_name}   @{ACCOUNT_NAMES}  ignore_case=false

  :FOR  ${index}  IN RANGE  ${length}
  \    ${listTexts}                               std.Set Variable  ${BROWSE_SCREEN_TEXTS}[${index}]
  \    Validate strings on screen                 ${listTexts}

  std.Sleep                                       ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/browse/browse_screen.png

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
  Shutdown android virtual device
  Shutdown appium server

Shutdown android virtual device
  ${command}                                      std.Set Variable  adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done
  process.Run Process                             ${command}  shell=true

Start android virtual device
  ${command}                                      std.Set Variable  %{ANDROID_HOME}/emulator/emulator -avd ${GLOBAL_AVD} &
  process.Run Process                             ${command}  shell=true  stdout=/dev/null  stderr=/dev/null

Shutdown appium server
  ${command}                                      std.Set Variable  ps -ef | grep appium | grep -v grep | awk '{print $2}' | xargs kill -9
  process.Run Process                             ${command}  shell=true

Start appium server
  ${command}                                      std.Set Variable  appium --session-override --reboot &
  process.Run Process                             ${command}  shell=true  stdout=/dev/null  stderr=/dev/null

Validate strings on screen
    [Documentation]                                   
    [Arguments]                                   @{texts_to_validate}
    :FOR  ${index}  ${text}  IN ENUMERATE         @{texts_to_validate}
    \    appium.Page Should Contain Text          ${text}   loglevel=DEBUG  

Validate landing screen
  appium.Wait Until Page Contains Element         ${SAB_LOGO}   ${TIMEOUT}
  ${go_to_login_button_text}                      appium.Get Text  ${BTN_GO_TO_LOGIN}
  ${go_to_signup_button_text}                     appium.Get Text  ${BTN_CREATE_ACCOUNT}
  std.Should Be Equal                             ${go_to_login_button_text}  ${LANDING_LOGIN_BUTTON_TEXT}  ignore_case=true
  std.Should Be Equal                             ${go_to_signup_button_text}  ${LANDING_SIGNUP_BUTTON_TEXT}  ignore_case=true
  std.Sleep                                       ${SCREENSHOT_SLEEP}
  #appium.Capture Page Screenshot                  ${LOGDIR}/screenshots/landing/screenshot.png