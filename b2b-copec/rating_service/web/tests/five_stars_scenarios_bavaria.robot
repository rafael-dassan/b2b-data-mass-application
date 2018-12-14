*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test

*** Test Case ***
5 Stars Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select a poc
  When the rating service modal is displayed
    And I select five stars
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select a poc
  When the rating service modal is displayed
    And I select five stars
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

5 Stars With Comment - Single Account User
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
  When the rating service modal is displayed
    And I select five stars
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed