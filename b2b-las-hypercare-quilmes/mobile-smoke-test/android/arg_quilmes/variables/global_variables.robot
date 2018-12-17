*** Variables ***

# Appium capabilities
${GLOBAL_APPIUM_SERVER_ADDRESS}  http://localhost:4723/wd/hub
${GLOBAL_PLATFORM_NAME}          Android
${GLOBAL_PLATFORM_VERSION}       9
${GLOBAL_DEVICE_NAME}            emulator-5554
${GLOBAL_APPLICATION_APK}        ${CURDIR}/../apk/app-argentina-debug.apk
${GLOBAL_APP_ACTIVITY}           com.abinbev.android.tapwiser.app.StartupActivity
${GLOBAL_APP_PACKAGE}            com.abinbev.android.tapwiser.argentina.debug
${GLOBAL_AVD}                    Nexus_5X_API_28
${GLOBAL_AUTOMATION_NAME}        UiAutomator2
${KILL_EMULATOR_COMMAND}         std.Set Variable  adb emu kill

# Results directory
${LOGDIR}                        ${CURDIR}/../results

# Application environments
${GLOBAL_ENVIRONMENTS}           std.Create List  Static Prod PreProd Qa Dev

# Home screen elements
${BTN_GO_TO_LOGIN}               id=logIn
${BTN_CREATE_ACCOUNT}            id=createAccount
${TEST_ENVIRONMENT}              PreProd
${TV_APP_NAME}                   id=logoText

# Browse screen elements
${HAMBURGUER_MENU}               xpath=//android.widget.ImageButton[@content-desc="Menu btn"]
${SEARCH}                        accessibility_id=Search All
${BROWSE_VIEW}                   id=browse_recyclerview
${TV_CATGORY_TITLE}              id=title

# Time
${TIMEOUT}                       50s
${SCREENSHOT_SLEEP}              200ms
${BOOTSTRAP_SLEEP}               5s