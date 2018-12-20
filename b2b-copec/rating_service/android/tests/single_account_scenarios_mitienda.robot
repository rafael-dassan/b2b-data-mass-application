*** Settings ***
Resource        ../resources/common_resources.robot
Suite Setup		Bootstrap test environment          ${APP_MITIENDA}    ${APP_PACKAGE_MITIENDA}
Suite Teardown  Close Application

Test Setup      Launch Application
Test Teardown   End Test    ${MS_RATING_URL}      ${JWT_MITIENDA_SINGLE}     ${CUSTID_MITIENDA_SINGLE}     ${USE_CASE_ID_MITIENDA_SINGLE}   ${COUNTRY_MITIENDA}     ${JWT_ADMIN}
*** Test Case ***

1 Star and 3 Tags With Comment - Single Account User
  [Tags]  Android   B2BCOPEC-859  MITIENDA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_MITIENDA_SINGLE}   ${PASSWORD_MITIENDA_SINGLE}
    And I finish the onboard
  When the rating service screen is displayed
    And I select a star   1
    And I select three tags                         ${TAG_1}  ${TAG_2}  ${TAG_3}
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed

2 Star and 3 Tags With Comment - Single Account User
  [Tags]  Android   B2BCOPEC-859   MITIENDA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_MITIENDA_SINGLE}   ${PASSWORD_MITIENDA_SINGLE}
    And I finish the onboard
  When the rating service screen is displayed
    And I select a star   2
    And I select three tags                         ${TAG_1}  ${TAG_2}  ${TAG_3}
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed

5 Stars with Comment - Single Account User
  [Tags]  Android   B2BCOPEC-859  MITIENDA
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_MITIENDA_SINGLE}   ${PASSWORD_MITIENDA_SINGLE}
    And I finish the onboard
  When the rating service screen is displayed
    And I select a star   5
    And I input a comment
    And I click on submit
  Then the thank you screen should be displayed 