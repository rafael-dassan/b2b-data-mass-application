*** Settings ***
Resource    ${CURDIR}/../resources/libraries.robot

*** Keywords ***
Begin Web Test
    selenium.Open Browser                about:blank                                               chrome

End Web Test
    selenium.Close Browser

Validate strings on screen
    [Documentation]                      Validating i18n text messages in POC selection screen.
    [Arguments]                          @{texts_to_validate}
    :FOR  ${index}  ${text}  IN ENUMERATE  @{texts_to_validate}
    \    selenium.Page Should Contain    ${text}

