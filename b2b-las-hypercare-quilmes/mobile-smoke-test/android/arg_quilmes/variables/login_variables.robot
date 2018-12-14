*** Variables ***

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

# Credentials
# User with more than one POC
${VALID_USER_MORE_POCS}          386041@mailinator.com
${VALID_PASS_MORE_POCS}          Las12345
${TEST_POC}                      386041
# User with only one POC
${VALID_USER_ONE_POC}            jose.vieirajunior@ab-inbev.com
${VALID_PASS_ONE_POC}            Lasabinbev12345
# Invalid user
${INVALID_USER}                  invalid
${INVALID_PASSWORD}              invalid12345

# Messages
${LOGIN_DIALOG_BTN_MESSAGE}      CONFIRMAR
${TOTAL_TUTORIAL_SCREENS}        3