*** Settings ***
Documentation	  Tests to verify that the Login Feature succeed and 
...             failed correctly depending on the users credentials.

Resource		    ${CURDIR}/../helpers/quilmes_imports.robot

Suite Setup     Bootstrap test environment
Suite Teardown  Close App

Test Setup		  appium.Launch Application
Test Teardown	  appium.Quit Application

*** Test Cases ***
Scenario 01: Login successfully as user with multiple POCs
	[Tags]	high	las-automated-smoke-test  login
	Given I select the environment  ${QUILMES_TEST_ENV}
  When I login with my user credentials  ${QUILMES_USER}  ${QUILMES_PASSWORD}
		And I choose the POC  ${QUILMES_TEST_POC}
    And I navigate through all introduction screens  
  Then I will be redirected to browse screen

Scenario 02: Login successfully as user with one POC
	[Tags]	high	las-automated-smoke-test  login
	Given I select the environment  ${QUILMES_TEST_ENV}
  When I login with my user credentials  ${QUILMES_USER_SINGLE}  ${QUILMES_PASSWORD_SINGLE}
    And I navigate through all introduction screens
  Then I will be redirected to browse screen

Scenario 03: Login unsuccessfully with empty credentials
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${QUILMES_TEST_ENV}
  When I do not enter the login credentials  ${EMPTY}  ${EMPTY}
  Then The Login button must be disabled

Scenario 04: Login unsuccessfully with invalid email
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${QUILMES_TEST_ENV}
  When I login with invalid email  ${INVALID_USER}  ${QUILMES_PASSWORD}
  Then A login error message is displayed  

Scenario 05: Login unsuccessfully with invalid password
  [Tags]	high	las-automated-smoke-test  login
  Given I select the environment  ${QUILMES_TEST_ENV}
  When I login with invalid password  ${QUILMES_USER}  ${INVALID_PASSWORD}
  Then A login error message is displayed