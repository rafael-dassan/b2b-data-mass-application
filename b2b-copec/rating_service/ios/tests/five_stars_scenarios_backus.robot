*** Settings ***
Resource        ../resources/common_resources.robot



*** Test Case ***
Test 5 Stars Without Comment
  [Tags]  iOS   B2BCOPEC-860
  Given I opened the Application    ${APP_BACKUS}       ${BUNDLE_BACKUS}
    And I set environment           ${ENV}
    And Click on login button
    And I enter my credentials      ${EMAIL_BACKUS}    ${PASSWORD_BACKUS} 
    And I click on Login
    And I select the POC            ${POC_BACKUS}

#   When the rating service modal is displayed
#     And I select five stars
#     And I click on submit
#   Then the thank you modal should be displayed

# Test 5 Stars With Comment
#   [Tags]  iOS   B2BCOPEC-860
#   Given I am logged
#   When the rating service modal is displayed
#     And I select five stars
#     And I filled the comment area
#     And I click on submit
#   Then the thank you modal should be displayed
