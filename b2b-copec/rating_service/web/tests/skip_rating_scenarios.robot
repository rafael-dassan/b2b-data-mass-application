*** Settings ***
Resource        ../resources/common_resources.robot
Test Teardown   Close Browser

*** Test Case ***
Skip Rating Bavaria
  [Tags]  WEB   B2BCOPEC-861
  Given I am logged     ${URL_BAVARIA}     ${EMAIL_BAVARIA}    ${PASSWORD_BAVARIA}
    And I select the POC  1
  When the rating service modal is displayed
    And I close the modal
  Then The rating should be skipped   ${URL_BAVARIA}      ${JWT_BAVARIA}     ${CUSTID_BAVARIA}     ${USE_CASE_ID_BAVARIA}    ${COUNTRY_BAVARIA}