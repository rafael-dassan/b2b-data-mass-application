*** Settings ***
Library     AppiumLibrary
Library     Collections
Library     Process
Resource    ./variables.robot
Library     ../helpers/ratingBarHelper.py


*** Keywords ***
I opened the Application
    Wait Until Element Is Visible           id=background_layout        timeout=60s

I set environment
    [Arguments]                             ${env}
    Swipe By Percent                        98  50    15    50  350
    Click Text                              ${env}
    Sleep                                   200ms
    Capture Page Screenshot
    Swipe By Percent                        50  50    99    50  350
    
Click on login button
    Click Element                           id=logIn
    Wait Until Page Contains Element        id=username


I enter my credentials
    [Arguments]                             ${email}            ${password}
    Input Text                              id=username         ${email}
    Input Password                          id=newPassword      ${password}
    Sleep                                   1
    Capture Page Screenshot
    Click Element                           id=login
          
I select the POC 
    [Arguments]                             ${poc}
    Wait Until Page Contains Element        id=userName         timeout=60s
    Click Text                              ${poc}
    I finish the onboard
    Capture Page Screenshot
    Wait Until Page Contains Element        id=ratingTxvDate    timeout=60s

I finish the onboard
    Wait Until Page Contains Element        id=tutorial_image       timeout=60s
    Swipe By Percent                        85  50    05  50  350
    Wait Until Page Contains Element        id=tutorial_image       timeout=60s
    Swipe By Percent                        85  50    05  50  350
    Wait Until Page Contains Element        id=start_button         timeout=60s
    Sleep                                   200ms
    Click Element                           id=start_button

the rating service screen is displayed
   Wait Until Page Contains Element         id=toolbar          timeout=60s

I select a star
    [Arguments]     ${stars}
    ${location}=    Get Element Location    id=ratingRbRating
    ${x}=           Get From Dictionary     ${location}   x
    ${y}=           Get From Dictionary     ${location}   y
    ${size}=        Get Element Size        id=ratingRbRating
    ${width}=       Get From Dictionary     ${size}     width
    ${x}=           get location star       ${stars}   ${x}     ${width}
    Click Element At Coordinates            ${x}    ${y}
   
I select one tag
    [Arguments]     ${tag}
    Click Text                              Wrong quantity
    Wait Until Page Contains Element        id=ratingSubmitButton

I select three tags
    [Arguments]     ${tag1}     ${tag2}     ${tag3}
    Click Text                              ${tag1}
    Sleep                                   1
    Click Text                              ${tag2}
    Sleep                                   1
    Click Text                              ${tag3}
    Sleep                                   1
    Wait Until Page Contains Element        id=ratingSubmitButton

I input a comment
    Input Text      ratingAddNotesText     problemas con el camión

I click on submit
    Sleep                                   200ms
    Capture Page Screenshot
    Click Element                           id=ratingSubmitButton      
    Wait Until Page Contains Element        id=sentCloseButton

the thank you screen should be displayed
    Wait Until Page Contains Element        id=sentCloseButton
    Capture Page Screenshot
    Click Element                           id=sentCloseButton
   
the submit button should appear disable
    Wait Until Page Contains Element        id=ratingSubmitButton
    Element Should Be Disabled              id=ratingSubmitButton

Bootstrap test environment
    [Arguments]         ${app}      ${package}
    ${command}          Set Variable  adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done
    Run Process         ${command}  shell=true
    ${command}          Set Variable  %{ANDROID_HOME}/emulator/emulator -avd ${DEVICE} &
    Run Process         ${command}  shell=true  stdout=/dev/null  stderr=/dev/null
    Sleep               ${BOOTSTRAP_SLEEP}
    ${command}          Set Variable  ps -ef | grep appium | grep -v grep | awk '{print $2}' | xargs kill -9
    Log                 ${command}  console=true
    Run Process         ${command}  shell=true
    ${command}          Set Variable  appium --session-override --reboot &
    Log                 ${command}  console=true
    Run Process         ${command}  shell=true  stdout=/dev/null  stderr=/dev/null
    Sleep               ${BOOTSTRAP_SLEEP}
    Open Application    http://localhost:4723/wd/hub    platformName=Android    platformVersion=9    deviceName=emulator-5554     app=${app}     appPackage=${package}  appActivity=com.abinbev.android.tapwiser.app.StartupActivity    automationName=UiAutomator2  avd=${DEVICE}
    Sleep               20s

I'm redirected to home screen
    Wait Until Page Contains Element        accessibility_id=Search All     timeout=60s

the rating service modal shouldnt be displayed
    Wait Until Page Does Not Contain        id=ratingIncludeToolbar     timeout=60s      