*** Settings ***
Library     SeleniumLibrary
Library     RequestsLibrary
Library     Collections
Library     BuiltIn
Library     JSONLibrary
Library     String
Resource    ./variables.robot

*** Keywords ***
End Web Test
    [Arguments]      ${url}      ${user_jwt}     ${user_account}     ${useCaseId}    ${country}     ${admin_jwt} 
    Remove the rating done      ${url}      ${user_jwt}     ${user_account}     ${useCaseId}     ${country}     ${admin_jwt}
    Close Browser

I am logged 
    [Arguments]                             ${url}      ${email}    ${password}
    Open Login Page                         ${url}
    Input Login and Password                ${email}    ${password}
    Click on LOG IN button
    
Open Login Page
    [Arguments]                             ${url}
    Open Browser                            ${url}      ${BROWSER}
    Wait Until Page Contains                Ingresa
    Sleep                                   500ms
    Capture Page Screenshot                # login_page.png

Input Login and Password
    [Arguments]                             ${email}            ${password}
    Input Text                              //*[@id="email"]    ${email}
    Input Password                          //*[@id="pass"]     ${password}

Click on LOG IN button
    Sleep                                   500ms
    Capture Page Screenshot                 #user_and_password.png
    Click Button                            //*[@id="send2"]

I closed the novedad modal    
    Wait Until Page Contains Element        class:box-modal     timeout=50s
    Sleep                                   10s   
    Click Element                           class:btn-messages
    Wait Until Page Contains Element        id:ui-id-5          timeout=50s

I'm redirected to home screen
    Wait Until Page Contains Element        //*[@id="search"]
    Sleep                                   20

the rating service modal shouldnt be displayed
    Wait Until Element Is Not Visible       //*[@id="rating-my-service"]/div/div/div

the rating service modal is displayed
    Wait Until Page Contains Element        //*[@id="rating-my-service"]/div/div/div    timeout=50s
    Sleep                                   500ms
    Capture Page Screenshot                 #modal_displayed.png

I filled the comment area
    Input Text                              //*[@id="option-anwser"]    Teste 
    ${textArea}=       Get Value            //*[@id="option-anwser"]
    Should Be Equal As Strings              ${textArea}   Teste
    Sleep                                   500ms
    Capture Page Screenshot                 #comment_area_filled.png   

I click on submit
    Element Should Be Enabled               //*[@id="rate-form"]/button
    Sleep                                   500ms
    Capture Page Screenshot                 #options_selected_modal.png
    Click Button                            //*[@id="rate-form"]/button

the thank you modal should be displayed
    Wait Until Element Is Visible           //*[@id="rating-my-service"]/div/div/div/div[3]/p[1]/button
    Sleep                                   500ms
    Capture Page Screenshot                 #thank_you.png
    Click Element                           //*[@id="rating-my-service"]/div/div/div/div[3]/p[1]/button

the submit button should be disabled
    Element Should Be Disabled              //*[@id="rate-form"]/button
    Sleep                                   500ms
    Capture Page Screenshot                 #submit_button_disabled.png

I select one tag
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[1]

I select three tags
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[1]
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[2]
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[3]
    Sleep                                   2

I select a star
    [Arguments]     ${star}
    Wait Until Page Contains Element        //*[@id="rate-form"]/div[1]/div/a[${star}]        timeout=50s
    Click Element                           //*[@id="rate-form"]/div[1]/div/a[${star}]

I select the POC
    [Arguments]                             ${pocPosition}
    Sleep                                   5s
    Wait Until Page Contains Element        //*[@id="choose-account"]
    Click Element                           //*[@id="login-association"]/div/div[1]/div[${pocPosition}]
    Sleep                                   500ms
    Capture Page Screenshot                 #poc_selected.png
    Click Button                            //*[@id="choose-account"]

I close the modal
    Click Element                           //*[@id="rating-my-service"]/div/div/div/div[1]/a/i
    Page Should Contain Element             id:search
    Capture Page Screenshot
    Sleep                                   5s

The rating should be skipped
    Set Log Level   TRACE
    [Arguments]     ${url}      ${user_jwt}     ${accountId}     ${useCaseId}    ${country}
    &{headers}=     Create Dictionary              requestTraceId    12341234    Authorization  ${user_jwt}
    Create Session	rating	    ${url}      disable_warnings=1
    ${resp}=        Get Request     rating      /?country=${country}&useCaseType=ORDER&accountId=${accountId}&useCaseId=${useCaseId}&page=1&pageSize=10   headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}     200
    ${json_object}          Set Variable     ${resp.json()}
    Log To Console          ${json_object}
    ${skipped_array}	            Get Value From Json	${json_object}      $.content[0].skipped
    ${skipped}              Set Variable     ${skipped_array}[0] 
    Should Be Equal As Strings  ${skipped}     true

And I already rated my order
    [Arguments]     ${url}      ${user_jwt}     ${accountId}     ${useCaseId}    ${country}
    &{headers}=     Create Dictionary              requestTraceId    12341234    Authorization  ${user_jwt}
    Create Session	rating	    ${url}      disable_warnings=1
    ${resp}=        Get Request     rating      /?country=${country}&useCaseType=ORDER&accountId=${accountId}&useCaseId=${useCaseId}&page=1&pageSize=10   headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}     200

Remove the rating done
    # [Arguments]     ${url}      ${accountId}    ${useCaseId}    ${country}     ${jwt}      
    [Arguments]     ${url}      ${user_jwt}     ${accountId}     ${useCaseId}    ${country}    ${admin_jwt} 
    &{headers}=     Create Dictionary              requestTraceId    12341234    Authorization  ${user_jwt}
    Create Session	rating	    ${url}      disable_warnings=1
    ${resp}=        Get Request     rating      /?country=${country}&useCaseType=ORDER&accountId=${accountId}&useCaseId=${useCaseId}&page=1&pageSize=10   headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}     200
    ${json_object}          Set Variable     ${resp.json()}
    # Log To Console          \n\nJSON OBJECT: ${json_object}
    ${rating_id_array}	    Get Value From Json	${json_object}      $.content[0].id 
    ${rating_id}            Set Variable     ${rating_id_array}[0] 
  
    &{headers}=       Create Dictionary     requestTraceId    12341234    Authorization     ${admin_jwt}
    ${resp}     Delete Request  rating      /${rating_id}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}     204