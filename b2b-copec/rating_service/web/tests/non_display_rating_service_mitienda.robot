*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   End Web Test

*** Test Case ***

Validate the non display of rating service modal
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged       ${URL_MITIENDA}     ${EMAIL_MITIENDA}    ${PASSWORD_MITIENDA}
    And I select a poc
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed

Validate the non display of rating service modal - Single Account User
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged       ${URL_MITIENDA}     ${EMAIL_MITIENDA_SINGLE}    ${PASSWORD_MITIENDA_SINGLE}
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed