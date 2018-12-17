*** Settings ***
Resource        ../resources/common_resources.robot
Suite Setup		Bootstrap test environment          ${APP_BACKUS}    ${APP_PACKAGE_BACKUS}
Suite Teardown  Close Application

Test Setup      Launch Application
Test Teardown   Quit Application

*** Test Case ***

Validate the non display of rating service modal
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  Android   B2BCOPEC-859   BACKUS
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BACKUS}   ${PASSWORD_BACKUS}
    And I select the POC                            ${POC_BACKUS}
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed

Validate the non display of rating service modal - Single Account User
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  [Tags]  Android   B2BCOPEC-859   BACKUS
  Given I opened the Application
    And I set environment                           ${ENV}
    And Click on login button
    And I enter my credentials                      ${EMAIL_BACKUS_SINGLE}   ${PASSWORD_BACKUS_SINGLE}
    And I finish the onboard
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed  