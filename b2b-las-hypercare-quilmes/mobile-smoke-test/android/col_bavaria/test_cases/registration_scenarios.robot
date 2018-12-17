# *** Settings ***
# Documentation   Tests to verify that the Registration Feature succeed and 
# ...             failed correctly depending on the new user credentials.

# Resource		${CURDIR}/../helpers/global_imports.robot

# Suite Setup     Bootstrap test environment
# Suite Teardown	Close App

# Test Setup		appium.Launch Application
# Test Teardown	appium.Quit Application

# *** Test Cases ***
# Scenario 01: Registration sucessfully
# 	[Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I register a new user      ${NEW_USER_FIRST_NAME}
#     ...                             ${NEW_USER_LAST_NAME}
#     ...                             ${NEW_USER_PHONE}
#     ...                             ${NEW_USER_CUSTOMERID}
#     ...                             ${NEW_USER_LEGALID}
#     Then The registration must be completed sucessfully

# Scenario 02: Validate registration with the input of invalid legal information
#     [Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I register a new user with invalid information 
#     Then The registration must not be completed

# Scenario 03: Validate registration with the input of an used email address
#     [Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I register a new user with an email previously used  ${NEW_USER_FIRST_NAME}
#     ...                                                       ${NEW_USER_LAST_NAME}
#     ...                                                       ${USED_EMAIL}
#     ...                                                       ${USED_EMAIL}
#     ...                                                       ${NEW_USER_PHONE}
#     ...                                                       ${NEW_USER_CUSTOMERID}
#     ...                                                       ${NEW_USER_LEGALID}
#     Then I must receive an email used error message

# Scenario 04: Validate registration with empty personal information
#     [Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I leave my personal information empty
#     Then I must not be able to go to the next registration step

# Scenario 05: Validate registration with empty account information
#     [Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I leave my account information empty
#     Then I must not be able to go to the next registration step

# Scenario 06: Validate wrong email format in personal information
# 	[Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I input an email with wrong format in personal information
#     Then I must receive an email format error message

# Scenario 07: Validate email match in personal information
#     [Tags]	high  las-automated-smoke-test  registration
#     Given I select the environment  ${TEST_ENVIRONMENT}
#     When I input different email addresses in personal information
#     Then I must receive an email match error message