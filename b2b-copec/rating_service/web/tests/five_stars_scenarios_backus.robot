*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test    ${MS_RATING_URL}      ${JWT_BACKUS}     ${CUSTID_BACKUS}     ${USE_CASE_ID_BACKUS}   ${COUNTRY_BACKUS}     ${JWT_ADMIN}

*** Test Case ***
5 Stars Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   5   
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   5   
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed