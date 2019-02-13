*** Variables ***

# Credentials
# User with more than one POC
${MULTIPLE_USER_EMAIL}         110920@mailinator.com
${MULTIPLE_USER_PASSWORD}      Teste123
${TEST_POC}                    110920
# User with only one POC
${SINGLE_USER_EMAIL}           110918@mailinator.com
${SINGLE_USER_PASSWORD}        Teste123
# Invalid user
${NON_EXISTENT_USER}           1212@mailinator.com
${INVALID_PASSWORD}            invalid12345
# Invalid e-mail format
${INVALID_EMAIL_FORMAT}        invalid

# Screen elements
${BTN_LOGIN}                   id=login
${ET_USERNAME}                 id=username
${ET_PASSWORD}                 id=newPassword
${LOGIN_FORM}                  id=signInForm
${ACCOUNT_VIEW}                id=account_recyclerview
${TP_LOGIN_ERROR_MESSAGE}      id=android:id/topPanel
${TV_LOGIN_ERROR_MESSAGE}      id=android:id/message
${BTN_LOGIN_CONFIRM}           id=android:id/button2
${TUTORIAL_IMAGE}              id=tutorial_image
${BTN_TUTORIAL_START}          id=start_button
${POCS_TO_CHOOSE}              id=drawerRecyclerview
${TV_EMAIL_INVALID}            id=usernameError