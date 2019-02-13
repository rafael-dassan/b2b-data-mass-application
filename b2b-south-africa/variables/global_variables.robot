*** Variables ***

# Appium capabilities
${GLOBAL_APPIUM_SERVER_ADDRESS}  http://localhost:4723/wd/hub
${GLOBAL_PLATFORM_NAME}          Android
${GLOBAL_PLATFORM_VERSION}       9
${GLOBAL_DEVICE_NAME}            emulator-5554
${GLOBAL_APPLICATION_APK}        ${CURDIR}/../apk/app-southAfrica-debug.apk
${GLOBAL_APP_ACTIVITY}           com.abinbev.android.tapwiser.app.StartupActivity
${GLOBAL_APP_PACKAGE}            com.abinbev.android.tapwiser.southAfrica.debug
${GLOBAL_AVD}                    Pixel_Pie
${GLOBAL_AUTOMATION_NAME}        UiAutomator2

# Results directory
${LOGDIR}                        ${CURDIR}/../results

# Application environments
@{GLOBAL_ENVIRONMENTS}           Static     Prod    PreProd     Qa      Dev

# South Africa test environment
${ZA_ENV}                        Qa

# Landing screen elements
${SAB_LOGO}                      id=logo
${BTN_GO_TO_LOGIN}               id=logIn
${BTN_CREATE_ACCOUNT}            id=createAccount

# Browse screen elements
${HAMBURGUER_MENU}               xpath=//android.widget.ImageButton[@content-desc="Menu btn"]
${SEARCH}                        accessibility_id=Search All
${BROWSE_VIEW}                   id=browse_recyclerview
${TV_CATGORY_TITLE}              id=title
${TV_COMPANY_NAME}               xpath=/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.TextView[2]

# Tutorial Screen
${TOTAL_TUTORIAL_SCREENS}        3

# Time
${TIMEOUT}                       50s
${SCREENSHOT_SLEEP}              200ms
${BOOTSTRAP_SLEEP}               5s