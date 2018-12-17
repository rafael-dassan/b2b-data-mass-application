*** Settings ***
Resource        ../resources/common_resources.robot
Suite Setup		Bootstrap test environment          ${APP_BAVARIA}    ${APP_PACKAGE_BAVARIA}
Suite Teardown  Close Application

Test Setup      Launch Application
Test Teardown   Quit Application

*** Test Case ***
2 Star and 1 Tag Without Comment
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   2
    And I select one tag                            ${TAG_1}
    And I click on submit
  Then the thank you screen should be displayed

2 Star and 1 Tag With Comment
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   2
    And I select one tag                            ${TAG_1}
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed 

2 Star and 3 Tags Without Comment
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   2
    And I select one tag                            ${TAG_1}
    And I click on submit
  Then the thank you screen should be displayed

2 Star and 3 Tags With Comment
  [Tags]  Android   B2BCOPEC-859   BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   2
    And I select three tags                         ${TAG_1}  ${TAG_2}  ${TAG_3}
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed

2 Star and 0 Tags 
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   2
  Then the submit button should appear disable

2 Star and 3 Tags With Comment - Single Account User
  [Tags]  Android   B2BCOPEC-859   BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA_SINGLE}   ${PASSWORD_BAVARIA_SINGLE}
    And I finish the onboard
  When the rating service screen is displayed
    And I select a star   2
    And I select three tags                         ${TAG_1}  ${TAG_2}  ${TAG_3}
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed