*** Settings ***
Resource        ../resources/common_resources.robot
Suite Setup		Bootstrap test environment          ${APP_BAVARIA}    ${APP_PACKAGE_BAVARIA}
Suite Teardown  Close Application

Test Setup      Launch Application
Test Teardown   Quit Application

*** Test Case ***
5 Stars without Comment
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   5
    And I click on submit
  Then the thank you screen should be displayed

5 Stars with Comment
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA}   ${PASSWORD_BAVARIA}
    And I select the POC                            ${POC_BAVARIA}
  When the rating service screen is displayed
    And I select a star   5
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed

5 Stars with Comment - Single Account User
  [Tags]  Android   B2BCOPEC-859  BAVARIA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BAVARIA_SINGLE}   ${PASSWORD_BAVARIA_SINGLE}
    And I finish the onboard
  When the rating service screen is displayed
    And I select a star   5
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed  