*** Settings ***
Library     SeleniumLibrary
Resource    ./variables.robot

*** Keywords ***
End Web Test
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
    Sleep                                   200ms
    Capture Page Screenshot                 login_page.png

Input Login and Password
    [Arguments]                             ${email}            ${password}
    Input Text                              //*[@id="email"]    ${email}
    Input Password                          //*[@id="pass"]     ${password}

Click on LOG IN button
    Sleep                                   200ms
    Capture Page Screenshot                 user_and_password.png
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
    Wait Until Element Is Not Visible       //*[@id="rating-my-service"]/div/div/div    timeout=50s

the rating service modal is displayed
    Wait Until Page Contains Element        //*[@id="rating-my-service"]/div/div/div    timeout=50s                   

I filled the comment area
    Input Text                              //*[@id="option-anwser"]    Teste 
    ${textArea}=       Get Value            //*[@id="option-anwser"]
    Should Be Equal As Strings              ${textArea}   Teste
    Sleep                                   200ms
    Capture Page Screenshot                 comment_area_filled.png   

I click on submit
    Click Button                            //*[@id="rate-form"]/button

the thank you modal should be displayed

the submit button should be disabled
    Element Should Be Disabled              //*[@id="rate-form"]/button
    Sleep                                   200ms
    Capture Page Screenshot                 submit_button_disabled.png

I select one tag
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[1]
    Sleep                                   200ms
    Capture Page Screenshot                 one_tag_selected.png

I select three tags
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[1]
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[2]
    Click Element                           //*[@id="rate-form"]/div[2]/div/label[3]
    Sleep                                   200ms
    Capture Page Screenshot                 three_tags_selected.png
    Sleep                                   2

I select a star
    [Arguments]     ${star}
    Wait Until Page Contains Element        //*[@id="rate-form"]/div[1]/div/a[${star}]        timeout=50s
    Click Element                           //*[@id="rate-form"]/div[1]/div/a[${star}]
    Element Should Be Enabled               //*[@id="rate-form"]/button
    Sleep                                   200ms
    Capture Page Screenshot                 five_stars_selected.png

I select the POC
    [Arguments]     ${poc}
    Wait Until Page Contains Element        //*[@id="choose-account"]
    Click Element                           //*[@id="login-association"]/div/div[1]/div[2]
    Click Button                            //*[@id="choose-account"]