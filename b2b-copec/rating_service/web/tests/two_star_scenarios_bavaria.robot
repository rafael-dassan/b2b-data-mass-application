*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test    ${MS_RATING_URL}      ${JWT_BAVARIA}     ${CUSTID_BAVARIA}     ${USE_CASE_ID_BAVARIA}   ${COUNTRY_BAVARIA}    ${JWT_ADMIN}

*** Test Case ***
2 Stars 1 Tag Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   2   
    And I select one tag
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 1 Tag With Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   2
    And I select one tag
    And I filled the comment area
    And I click on submit
  Then the thank you modal should be displayed

2 Stars 3 Tags Without Comment
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select the POC  1
  When the rating service modal is displayed
    And I select a star   2
    And I select three tags
    And I click on submit
  Then the thank you modal should be displayed

# 2 Stars 0 Tag Without Comment
#   [Tags]  WEB   B2BCOPEC-861
#   Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
#     And I select a poc  ${POC_BAVARIA}
#   When the rating service modal is displayed
#     And I select two stars
#   Then the submit button should be disabled

# 2 Stars 3 Tags With Comment - Single Account User
#   [Tags]  WEB   B2BCOPEC-861
#   Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
#   When the rating service modal is displayed
#     And I select two stars
#     And I select three tags
#     And I filled the comment area
#     And I click on submit
#   Then the thank you modal should be displayed