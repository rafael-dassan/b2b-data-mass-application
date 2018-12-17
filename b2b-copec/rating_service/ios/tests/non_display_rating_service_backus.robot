*** Settings ***
Resource        ../resources/common_resources.robot

*** Test Case ***

Validate the non display of rating service modal
  [Documentation]   This scenario validated if the rating service respeact the precondition of have a order status delivered
  Given I opened the Application    ${APP_BACKUS}      ${BUNDLE_BACKUS}
    And I set environment           ${ENV}
    And Click on login button
    And I enter my credentials      ${EMAIL_BACKUS}    ${PASSWORD_BACKUS} 
    And I click on Login
    And I select the POC            ${POC_BACKUS}
  When I'm redirected to home screen
  Then the rating service modal shouldnt be displayed