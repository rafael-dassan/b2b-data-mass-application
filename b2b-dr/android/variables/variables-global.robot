*** Variables ***
# Device port number should be between 5554 and 5584

# Appium capabilities
${APPIUM_SERVER_ADDRESS}    http://localhost:4723/wd/hub
${PLATFORM_NAME}            Android
${PLATFORM_VERSION}         8.1
#${PLATFORM_VERSION}        8.0.0
#${PLATFORM_VERSION}        5.0.1
#${PLATFORM_VERSION}        8.1.0
#${DEVICE_NAME}             LG K10 LTE
#${DEVICE_NAME}             RQ3005NCZ8
#${DEVICE_NAME}             SM-G903M
#${DEVICE_NAME}             Samsung GT-I9515L
#${DEVICE_NAME}             Moto G_5s_Plus
${DEVICE_NAME}              emulator-5554
${APK}                      ${CURDIR}/../apks/app-dominicanRepublic-debug.apk
${APP_ACTIVITY}             com.abinbev.android.tapwiser.app.StartupActivity
${APP_PACKAGE}              com.abinbev.android.tapwiser.dominicanRepublic.debug
${AVD}                      Pixel_Oreo
${AUTOMATION_NAME}          uiautomator2

${KILL_PROCESS_COMMAND}     ps aux | pgrep -f pattern | xargs kill $SIGTERM