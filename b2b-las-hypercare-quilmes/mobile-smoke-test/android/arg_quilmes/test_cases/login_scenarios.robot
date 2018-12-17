*** Settings ***
Documentation	  Tests to verify that the Login Feature succeed and 
...             failed correctly depending on the users credentials.

Resource		    ${CURDIR}/../helpers/global_imports.robot

Suite Setup     Bootstrap test environment
Suite Teardown  Close App

Test Setup		  appium.Launch Application
Test Teardown	  appium.Quit Application

*** Test Cases ***
Scenario 01: Login successfully as user with multiple POCs
	[Tags]	high	las-automated-smoke-test  login
	Given I select the environment  ${TEST_ENVIRONMENT}
  When I login with my user credentials  ${VALID_USER_MORE_POCS}  ${VALID_PASS_MORE_POCS}
		And I choose the POC  ${TEST_POC}
    And I navigate through all introduction screens  
  Then I will be redirected to browse screen

Scenario 02: Login successfully as user with one POC
	[Tags]	high	las-automated-smoke-test  login
	Given I select the environment  ${TEST_ENVIRONMENT}
  When I login with my user credentials  ${VALID_USER_ONE_POC}  ${VALID_PASS_ONE_POC}
    And I navigate through all introduction screens
  Then I will be redirected to browse screen

Scenario 03: Login unsuccessfully with empty credentials
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${TEST_ENVIRONMENT}
  When I do not enter the login credentials  ${EMPTY}  ${EMPTY}
  Then The Login button must be disabled

Scenario 04: Login unsuccessfully with invalid email
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${TEST_ENVIRONMENT}
  When I login with invalid email  ${INVALID_USER}  ${VALID_PASS_MORE_POCS}
  Then A login error message is displayed  

Scenario 05: Login unsuccessfully with invalid password
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${TEST_ENVIRONMENT}
  When I login with invalid password  ${VALID_USER_MORE_POCS}  ${INVALID_PASSWORD}
  Then A login error message is displayed