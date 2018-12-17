*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test

*** Test Case ***
2 Stars 1 Tag Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
  When the rating service modal is displayed
    And I select two stars
    And I select one tag
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 1 Tag With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
  When the rating service modal is displayed
    And I select two stars
    And I select one tag
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 3 Tags Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
  When the rating service modal is displayed
    And I select two stars
    And I select three tags
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 0 Tag Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS}    ${PASSWORD_BACKUS}
    And I select a poc  ${POC_BACKUS}
  When the rating service modal is displayed
    And I select two stars
  Then the submit button should be disabled

2 Stars 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BACKUS}     ${EMAIL_BACKUS_SINGLE}    ${PASSWORD_BACKUS_SINGLE}
  When the rating service modal is displayed
    And I select two stars
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed