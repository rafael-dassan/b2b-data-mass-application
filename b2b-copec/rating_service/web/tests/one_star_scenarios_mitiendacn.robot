*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test

*** Test Case ***
1 Star 1 Tag Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select a poc  ${POC_MITIENDA}
  When the rating service modal is displayed
    And I select one star
    And I select one tag
    And I click on submit
  Then the thank you modal should be displayed

1 Star 1 Tag With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select a poc  ${POC_MITIENDA}
  When the rating service modal is displayed
    And I select one star
    And I select one tag
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

1 Star 3 Tags Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select a poc  ${POC_MITIENDA}
  When the rating service modal is displayed
    And I select one star
    And I select three tags
    And I click on submit
  Then the thank you modal should be displayed

1 Star 0 Tag Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select a poc  ${POC_MITIENDA}
  When the rating service modal is displayed
    And I select one star
  Then the submit button should be disabled

1 Star 3 Tags With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
  When the rating service modal is displayed
    And I select one star
    And I select three tags
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed