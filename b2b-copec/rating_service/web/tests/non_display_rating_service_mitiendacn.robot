*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   Close Browser

*** Test Case ***

Validate the non display of rating service modal
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged       ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I already rated my order  ${URL_MITIENDA}      ${JWT_MITIENDA}     ${CUSTID_MITIENDA}     ${USE_CASE_ID_MITIENDA}    ${COUNTRY_MITIENDA}
    And I select the POC  1
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed

# Validate the non display of rating service modal - Single Account User
#   [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
#   [Tags]  WEB   B2BCOPEC-861
#   Given I am logged       ${URL_MITIENDA}     ${EMAIL_MITIENDA_SINGLE}    ${PASSWORD_MITIENDA_SINGLE}
#   When I'm redirected to home screen
#   Then the rating service modal shouldnt be displayed