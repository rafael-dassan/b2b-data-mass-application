*** Settings ***
Resource        ../resources/common_resources.robot
Suite Setup		Bootstrap test environment          ${APP_BAVARIA}    ${APP_PACKAGE_BAVARIA}
Suite Teardown  Close Application

Test Setup      Launch Application
Test Teardown   End Test    ${MS_RATING_URL}      ${JWT_BAVARIA}     ${CUSTID_BAVARIA}     ${USE_CASE_ID_BAVARIA}   ${COUNTRY_BAVARIA}     ${JWT_ADMIN}

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