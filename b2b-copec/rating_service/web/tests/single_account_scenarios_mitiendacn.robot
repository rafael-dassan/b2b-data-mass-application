*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test    ${MS_RATING_URL}      ${JWT_MITIENDA_SINGLE}     ${CUSTID_MITIENDA_SINGLE}     ${USE_CASE_ID_MITIENDA_SINGLE}     ${COUNTRY_MITIENDA}   ${JWT_ADMIN}

*** Test Case ***
5 Stars With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA_SINGLE}    ${PASSWORD_MITIENDA_SINGLE}
  When the rating service modal is displayed
    And I select a star   5
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

1 Star 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA_SINGLE}    ${PASSWORD_MITIENDA_SINGLE}
  When the rating service modal is displayed
    And I select a star     1
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA_SINGLE}    ${PASSWORD_MITIENDA_SINGLE}
  When the rating service modal is displayed
    And I select a star     2
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed