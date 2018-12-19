*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test    ${MS_RATING_URL}      ${JWT_MITIENDA}     ${CUSTID_MITIENDA}     ${USE_CASE_ID_MITIENDA}   ${COUNTRY_MITIENDA}     ${JWT_ADMIN}

*** Test Case ***
5 Stars Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   5   
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   5   
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed