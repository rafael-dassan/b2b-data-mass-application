*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   Close Browser

*** Test Case ***

Validate the non display of rating service modal
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged       ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I already rated my order  ${URL_BAVARIA}      ${JWT_BAVARIA}     ${CUSTID_BAVARIA}     ${USE_CASE_ID_BAVARIA}    ${COUNTRY_BAVARIA}
    And I select the POC  1
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed

# Validate the non display of rating service modal - Single Account User
#   [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
#   [Tags]  WEB   B2BCOPEC-861
#   Given I am logged       ${URL_BAVARIA}     ${EMAIL_BAVARIA_SINGLE}    ${PASSWORD_BAVARIA_SINGLE}
#   When I'm redirected to home screen
#   Then the rating service modal shouldnt be displayed