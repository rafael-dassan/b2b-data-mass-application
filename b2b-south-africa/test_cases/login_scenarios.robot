*** Settings ***
Documentation	  Tests to verify that the Login Feature succeed and 
...               failed correctly depending on the users credentials.

Resource		    ${CURDIR}/../helpers/global_imports.robot

Suite Setup     Bootstrap test environment
Suite Teardown  Close App

Test Setup		  appium.Launch Application
Test Teardown	  appium.Quit Application

*** Test Cases ***
# Scenario 01: Login successfully as user with multiple POCs
# 	[Tags]	high	za-automated-test  login
# 	Given I select the environment  ${ZA_ENV}
#   When I login with my user credentials  ${USER_EMAIL}  ${USER_PASSWORD}
# 		And I choose the POC  ${TEST_POC}
#     And I navigate through all introduction screens  
#   Then I will be redirected to browse screen

Scenario 02: Login successfully as user with one POC
	[Tags]	high	za-automated-test  login
	Given I select the environment  ${ZA_ENV}
  When I login with my user credentials  ${SINGLE_USER_EMAIL}  ${SINGLE_USER_PASSWORD}
    And I navigate through all introduction screens
  Then I will be redirected to browse screen

Scenario 03: Login unsuccessfully with empty credentials
  [Tags]	high	za-automated-test  login
  Given I select the environment  ${ZA_ENV}
  When I do not enter the login credentials  ${EMPTY}  ${EMPTY}
  Then The Login button must be disabled

# Scenario 04: Login unsuccessfully with invalid email format
#   [Tags]	high	za-automated-test  login
#   Given I select the environment  ${ZA_ENV}
#   When I login with invalid email  ${INVALID_EMAIL_FORMAT}  ${PASSWORD}
#   Then An invalid email format error message is displayed

# Scenario 05: Login unsuccessfully with non-existent email
#   [Tags]	high	za-automated-test  login
#   Given I select the environment  ${ZA_ENV}
#   When I login with invalid email  ${INVALID_EMAIL}  ${PASSWORD}
#   Then A login error message is displayed

# Scenario 06: Login unsuccessfully with invalid password
#   [Tags]	high	za-automated-test  login
#   Given I select the environment  ${ZA_ENV}
#   When I login with invalid password  ${EMAIL}  ${PASSWORD}
#   Then A login error message is displayed