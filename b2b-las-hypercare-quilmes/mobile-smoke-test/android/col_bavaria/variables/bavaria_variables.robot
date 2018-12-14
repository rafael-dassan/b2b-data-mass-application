*** Variables ***

# Appium capabilities
${GLOBAL_APPIUM_SERVER_ADDRESS}  http://localhost:4723/wd/hub
${GLOBAL_PLATFORM_NAME}          Android
${GLOBAL_PLATFORM_VERSION}       9
${GLOBAL_DEVICE_NAME}            emulator-5554
${GLOBAL_APPLICATION_APK}        ${CURDIR}/../apk/app-colombiaBavaria-debug.apk
${GLOBAL_APP_ACTIVITY}           com.abinbev.android.tapwiser.app.StartupActivity
${GLOBAL_APP_PACKAGE}            com.abinbev.android.tapwiser.colombiaBavaria.debug
${GLOBAL_AVD}                    Nexus_5X_API_28
${GLOBAL_AUTOMATION_NAME}        UiAutomator2
${KILL_EMULATOR_COMMAND}         std.Set Variable  adb emu kill

# Results directory
${LOGDIR}                        ${CURDIR}/../results

# Bavaria test environment
${BAVARIA_TEST_ENV}              Qa
