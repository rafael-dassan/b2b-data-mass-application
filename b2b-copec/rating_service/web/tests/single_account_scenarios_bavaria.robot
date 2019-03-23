*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test    ${MS_RATING_URL}      ${JWT_BAVARIA_SINGLE}     ${CUSTID_BAVARIA_SINGLE}     ${USE_CASE_ID_BAVARIA_SINGLE}     ${COUNTRY_BAVARIA}   ${JWT_ADMIN}

*** Test Case ***
5 Stars With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
  When the rating service modal is displayed
    And I select a star   5
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

1 Star 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
  When the rating service modal is displayed
    And I select a star     1
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
  When the rating service modal is displayed
    And I select a star     2
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed