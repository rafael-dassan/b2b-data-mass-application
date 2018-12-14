*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test

*** Test Case ***
5 Stars Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
    And I closed the novedad modal
  When the rating service modal is displayed
    And I select a star    5
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
    And I closed the novedad modal
  When the rating service modal is displayed
    And I select a star    5
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS_SINGLE}    ${PASSWORD_BACKUS_SINGLE}
    And I closed the novedad modal
  When the rating service modal is displayed
    And I select a star    5
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed