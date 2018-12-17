*** Variables ***

# Home screen elements
${BTN_GO_TO_LOGIN}               id=logIn
${BTN_CREATE_ACCOUNT}            id=createAccount

# Browse screen elements
${HAMBURGUER_MENU}               xpath=//android.widget.ImageButton[@content-desc="Menu btn"]
${SEARCH}                        accessibility_id=Search All
${BROWSE_VIEW}                   id=browse_recyclerview
${TV_CATGORY_TITLE}              id=title

# Application environments
${GLOBAL_ENVIRONMENTS}           std.Create List  Static Prod PreProd Qa Dev

# Messages
${bavaria_login_error_message}   Usuario o clave errada o su cuenta se ha desactivado temporalmente.\n\nv1.7.3
${quilmes_login_error_message}   Usuario o clave incorrecta. Por favor ingrese los datos de nuevo.
@{LOGIN_INVALID_MESSAGE}         ${bavaria_login_error_message}         ${quilmes_login_error_message}

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