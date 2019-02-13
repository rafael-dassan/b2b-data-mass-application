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
	[Tags]	high	za-auto  login
	Given I select the environment  ${ZA_ENV}
  When I login with my user credentials  ${MULTIPLE_USER_EMAIL}  ${MULTIPLE_USER_PASSWORD}
		And I choose the POC  ${TEST_POC}
    And I navigate through all introduction screens  
  Then I will be redirected to browse screen

Scenario 02: Login successfully as user with one POC
	[Tags]	high	za-auto  login
	Given I select the environment  ${ZA_ENV}
  When I login with my user credentials  ${SINGLE_USER_EMAIL}  ${SINGLE_USER_PASSWORD}
    And I navigate through all introduction screens
  Then I will be redirected to browse screen

Scenario 03: Login unsuccessfully with empty credentials
  [Tags]	high	za-auto  login
  Given I select the environment  ${ZA_ENV}
  When I do not enter the login credentials  ${EMPTY}  ${EMPTY}
  Then The Login button must be disabled

Scenario 04: Login unsuccessfully with invalid email format
  [Tags]	high	za-auto  login
  Given I select the environment  ${ZA_ENV}
  When I login with invalid email  ${INVALID_EMAIL_FORMAT}  ${SINGLE_USER_PASSWORD}
  Then A login error message is displayed

Scenario 05: Login unsuccessfully with non-existent email
  [Tags]	high	za-auto  login
  Given I select the environment  ${ZA_ENV}
  When I login with invalid email  ${NON_EXISTENT_USER}  ${SINGLE_USER_PASSWORD}
  Then A login error message is displayed

Scenario 06: Login unsuccessfully with invalid password
  [Tags]	high	za-auto  login
  Given I select the environment  ${ZA_ENV}
  When I login with invalid password  ${SINGLE_USER_EMAIL}  ${INVALID_PASSWORD}
  Then A login error message is displayed