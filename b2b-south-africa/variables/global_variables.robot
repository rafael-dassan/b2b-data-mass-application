*** Variables ***

# Appium capabilities
${GLOBAL_APPIUM_SERVER_ADDRESS}  http://localhost:4723/wd/hub
${GLOBAL_PLATFORM_NAME}          Android
${GLOBAL_PLATFORM_VERSION}       9
${GLOBAL_DEVICE_NAME}            emulator-5554
${GLOBAL_APPLICATION_APK}        ${CURDIR}/../apk/app-southAfrica-debug.apk
${GLOBAL_APP_ACTIVITY}           com.abinbev.android.tapwiser.app.StartupActivity
${GLOBAL_APP_PACKAGE}            com.abinbev.android.tapwiser.southAfrica.debug
${GLOBAL_AVD}                    Pixel
${GLOBAL_AUTOMATION_NAME}        UiAutomator2

# Results directory
${LOGDIR}                        ${CURDIR}/../results

# Bavaria test environment
${ZA_ENV}                        Qa

# Home screen elements
${BTN_GO_TO_LOGIN}               id=logIn
${BTN_CREATE_ACCOUNT}            id=createAccount

# Browse screen elements
${HAMBURGUER_MENU}               xpath=//android.widget.ImageButton[@content-desc="Menu btn"]
${SEARCH}                        accessibility_id=Search All
${BROWSE_VIEW}                   id=browse_recyclerview
${TV_CATGORY_TITLE}              id=title

# Application environments
@{GLOBAL_ENVIRONMENTS}           Static     Prod    PreProd     Qa      Dev
${ZA_ENV}                        Qa

# Messages
${LOGIN_DIALOG_BTN_MESSAGE}      CONFIRMAR
${TOTAL_TUTORIAL_SCREENS}        3
${bavaria_login_error_message}   Usuario o clave errada o su cuenta se ha desactivado temporalmente.\n\nv1.7.3
${quilmes_login_error_message}   Usuario o clave incorrecta. Por favor ingrese los datos de nuevo.
@{LOGIN_INVALID_MESSAGE}         ${bavaria_login_error_message}  ${quilmes_login_error_message}

# Time
${TIMEOUT}                       50s
${SCREENSHOT_SLEEP}              200ms
${BOOTSTRAP_SLEEP}               5s

#========================== LOGIN ==========================#
# Screen elements
${BTN_LOGIN}                     id=login
${ET_USERNAME}                   id=username
${ET_PASSWORD}                   id=newPassword
${LOGIN_FORM}                    id=signInForm
${ACCOUNT_VIEW}                  id=account_recyclerview
${TP_LOGIN_ERROR_MESSAGE}        id=android:id/topPanel
${TV_LOGIN_ERROR_MESSAGE}        id=android:id/message
${BTN_LOGIN_CONFIRM}             id=android:id/button2
${TUTORIAL_IMAGE}                id=tutorial_image
${BTN_TUTORIAL_START}            id=start_button
${POCS_TO_CHOOSE}                id=drawerRecyclerview
${TV_EMAIL_INVALID}              id=usernameError