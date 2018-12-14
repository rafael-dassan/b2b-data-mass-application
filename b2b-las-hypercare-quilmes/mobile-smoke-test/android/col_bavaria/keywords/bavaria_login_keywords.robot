*** Keywords ***

An invalid email format error message is displayed
    appium.Wait Until Page Contains Element     ${TV_EMAIL_INVALID}   ${TIMEOUT}
    appium.Element Should Contain Text          ${TV_EMAIL_INVALID}   ${LOGIN_EMAIL_FORMAT_MESSAGE}
    appium.Capture Page Screenshot              login_email_format_error_message.png