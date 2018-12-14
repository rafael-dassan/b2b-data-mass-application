*** Settings ***
Documentation	  Tests to verify that the Login Feature succeed and 
...             failed correctly depending on the users credentials.

Resource		    ${CURDIR}/../helpers/bavaria_imports.robot

Suite Setup     Bootstrap test environment
Suite Teardown  Close App

Test Setup		  appium.Launch Application
Test Teardown	  appium.Quit Application

*** Test Cases ***
Scenario 01: Login successfully as user with multiple POCs
	[Tags]	high	bavaria-automated-smoke-test  login
	Given I select the environment  ${BAVARIA_TEST_ENV}
  When I login with my user credentials  ${EMAIL_BAVARIA}  ${PASSWORD_BAVARIA}
		And I choose the POC  ${TEST_POC_BAVARIA}
    And I navigate through all introduction screens  
  Then I will be redirected to browse screen

# # Scenario 02: Login successfully as user with one POC
# # 	[Tags]	high	bavaria-automated-smoke-test  login
# # 	Given I select the environment  ${TEST_ENVIRONMENT}
# #   When I login with my user credentials  ${VALID_USER_ONE_POC}  ${VALID_PASS_ONE_POC}
# #     And I navigate through all introduction screens
# #   Then I will be redirected to browse screen

Scenario 03: Login unsuccessfully with empty credentials
  [Tags]	high	bavaria-automated-smoke-test  login
  Given I select the environment  ${BAVARIA_TEST_ENV}
  When I do not enter the login credentials  ${EMPTY}  ${EMPTY}
  Then The Login button must be disabled

Scenario 04: Login unsuccessfully with invalid email format
  [Tags]	high	bavaria-automated-smoke-test  login
  Given I select the environment  ${BAVARIA_TEST_ENV}
  When I login with invalid email  ${INVALID_EMAIL_FORMAT}  ${PASSWORD_BAVARIA}
  Then An invalid email format error message is displayed

Scenario 05: Login unsuccessfully with non-existent email
  [Tags]	high	bavaria-automated-smoke-test  login
  Given I select the environment  ${BAVARIA_TEST_ENV}
  When I login with invalid email  ${INVALID_EMAIL}  ${PASSWORD_BAVARIA}
  Then A login error message is displayed

Scenario 06: Login unsuccessfully with invalid password
  [Tags]	high	bavaria-automated-smoke-test  login
  Given I select the environment  ${BAVARIA_TEST_ENV}
  When I login with invalid password  ${EMAIL_BAVARIA}  ${INVALID_PASSWORD}
  Then A login error message is displayed