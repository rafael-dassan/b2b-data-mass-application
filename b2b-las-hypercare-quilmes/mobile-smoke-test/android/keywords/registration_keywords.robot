*** Keywords ***

I register a new user with invalid information
    I register a new user                               ${NEW_USER_FIRST_NAME}  ${NEW_USER_LAST_NAME}  ${NEW_USER_PHONE}
    ...                                                 ${INVALID_CUSTOMERID}  ${INVALID_LEGALID}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/registration_invalid_information.png
    appium.Click Element                                ${BTN_SOUNDS_GOOD}

I register a new user
    [Arguments]                                         ${first_name}  ${last_name}  ${phone}
    ...                                                 ${customer_id}  ${legal_id}
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Generate Random Email
    Input Personal Information                          ${first_name}  ${last_name}  ${random_email}   
    ...                                                 ${random_email}  ${phone}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}
    Input Account Information                           ${customer_id}  ${legal_id}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}
    
    # Last screen of account registration
    appium.Wait Until Page Contains Element             ${BTN_SOUNDS_GOOD}  ${TIMEOUT}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/registration_last_screen.png

I register a new user with an email previously used
    [Arguments]                                         ${first_name}  ${last_name}  ${email}    
    ...                                                 ${email_confirmation}  ${phone}
    ...                                                 ${customer_id}  ${legal_id}
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Input Personal Information                          ${first_name}  ${last_name}  ${email}   
    ...                                                 ${email_confirmation}  ${phone}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}
    Input Account Information                           ${customer_id}  ${legal_id}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}

    # Last screen of account registration
    appium.Wait Until Page Contains Element             ${BTN_SOUNDS_GOOD}  ${TIMEOUT}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/registration_last_screen.png


Input Personal Information
    [Arguments]                                         ${first_name}  ${last_name}  ${email}    
    ...                                                 ${email_confirmation}  ${phone}
    appium.Wait Until Page Contains Element             ${ET_FIRST_NAME}  ${TIMEOUT}
    appium.Input Text                                   ${ET_FIRST_NAME}  ${first_name}
    appium.Input Text                                   ${ET_LAST_NAME}  ${last_name}
    appium.Input Text                                   ${ET_EMAIL_ADDRESS}  ${email}
    appium.Input Text                                   ${ET_EMAIL_ADDRESS_CONFIRM}  ${email_confirmation}
    appium.Input Text                                   ${ET_PHONE_NUMBER}  ${phone}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/input_personal_information.png

Input Account Information
    [Arguments]                                         ${customer_id}  ${legal_id}
    appium.Wait Until Page Contains Element             ${ET_CUSTOMER_ID}  ${TIMEOUT}
    appium.Input Text                                   ${ET_CUSTOMER_ID}  ${customer_id}
    appium.Input Text                                   ${ET_LEGAL_ID}  ${legal_id}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/input_account_information.png

I leave my personal information empty
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Input Personal Information                          ${EMPTY}  ${EMPTY}  ${EMPTY}  ${EMPTY}  ${EMPTY}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/empty_personal_information.png
    
I leave my account information empty
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Input Personal Information                          ${NEW_USER_FIRST_NAME}  ${NEW_USER_LAST_NAME}  
    ...                                                 ${USED_EMAIL}  ${USED_EMAIL}   
    ...                                                 ${NEW_USER_PHONE}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}
    Input Account Information                           ${EMPTY}  ${EMPTY}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/empty_account_information.png

I input an email with wrong format in personal information
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Input Personal Information                          ${NEW_USER_FIRST_NAME}  ${NEW_USER_LAST_NAME}  
    ...                                                 ${EMAIL_WRONG_FORMAT}
    ...                                                 ${USED_EMAIL}  ${NEW_USER_PHONE}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}

I must not be able to go to the next registration step
    Element Should Be Disabled                          ${BTN_NEXT_REGISTRATION_STEP}

I must receive an email format error message
    appium.Wait Until Page Contains Element             ${TV_EMAIL_FORMAT_ERROR}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_EMAIL_FORMAT_ERROR}  ${EMAIL_FORMAT_ERROR_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/email_format_error_message.png
    

I input different email addresses in personal information 
    appium.Click Element                                ${BTN_CREATE_ACCOUNT}
    Input Personal Information                          ${NEW_USER_FIRST_NAME}  ${NEW_USER_LAST_NAME}  ${USED_EMAIL}
    ...                                                 ${EMAIL_DO_NOT_MATCH}  ${NEW_USER_PHONE}
    appium.Click Element                                ${BTN_NEXT_REGISTRATION_STEP}

I must receive an email match error message
    appium.Wait Until Page Contains Element             ${TV_EMAIL_MATCH_ERROR}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_EMAIL_MATCH_ERROR}  ${EMAIL_MATCH_ERROR_MESSAGE}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/email_match_error_message.png

The registration must not be completed
    appium.Wait Until Page Contains Element             ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}
    ${errorMessage}                                     appium.Get Text  ${TV_REGISTRATION_MESSAGE}
    std.Should Contain Any                              ${errorMessage}  ${USER_NOT_FOUND_ERROR_MESSAGE}  ignore_case=false
    appium.Element Should Contain Text                  ${BTN_REGISTRATION_CONFIRM}    
    ...                                                 ${REGISTRATION_DIALOG_BTN_MESSAGE}  ${TIMEOUT}
    std.Sleep                                           ${SCREENSHOT_SLEEP}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/registration_error_message.png
    appium.Click Element                                ${BTN_REGISTRATION_CONFIRM}
    appium.Wait Until Page Does Not Contain Element     ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}

The registration must be completed sucessfully
    appium.Click Element                                ${BTN_SOUNDS_GOOD}
    appium.Wait Until Page Contains Element             ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_REGISTRATION_MESSAGE}  ${SUCCESSFULLY_REGISTRATION_MESSAGE}  ${TIMEOUT}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/registration_successfully.png
    appium.Click Element                                ${BTN_REGISTRATION_CONFIRM}
    appium.Wait Until Page Does Not Contain Element     ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}

I must receive an email used error message
    appium.Click Element                                ${BTN_SOUNDS_GOOD}
    appium.Wait Until Page Contains Element             ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}
    appium.Element Should Contain Text                  ${TV_REGISTRATION_MESSAGE}  ${USED_EMAIL_MESSAGE}  ${TIMEOUT}
    appium.Capture Page Screenshot                      ${LOGDIR}/screenshots/registration/used_email_error_message.png
    appium.Click Element                                ${BTN_REGISTRATION_CONFIRM}
    appium.Wait Until Page Does Not Contain Element     ${TP_REGISTRATION_MESSAGE}  ${TIMEOUT}

Generate Random Email
    ${email_first_element}                              str.Generate Random String  5  [LOWER]
    ${random_email}                                     std.Catenate  ${email_first_element}@test.com
    std.Set Suite Variable                              ${random_email}
    std.Log                                             \nRegistration email: ${random_email}     console=yes