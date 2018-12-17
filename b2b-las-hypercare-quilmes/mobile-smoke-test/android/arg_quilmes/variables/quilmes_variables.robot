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

# Results directory
${LOGDIR}                        ${CURDIR}/../results

# Quilmes test environment
${QUILMES_TEST_ENV}              PreProd