*** Settings ***
Documentation	Tests to verify that the Manage Account Feature succeed and 
...             failed correctly depending on the users credentials.

Resource		${CURDIR}/../helpers/global_imports.robot

Suite Setup     Bootstrap test environment
Suite Teardown	Close App

Test Setup		appium.Launch Application
Test Teardown	appium.Quit Application

*** Test Cases ***

Scenario 01: Password change successfully
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I change my password  ${VALID_PASS_MORE_POCS}  ${NEW_PASSWORD}  ${NEW_PASSWORD}
    Then The password must be changed successfully

Scenario 02: Validate password change with empty information
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I do not enter the passwords  ${EMPTY}  ${EMPTY}  ${EMPTY}
    Then The Change Password button must be disabled

Scenario 03: Validate password change with new passwords not matching
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I enter different passwords  ${VALID_PASS_MORE_POCS}  ${NEW_PASSWORD}  ${NEW_PASSWORD_NOT_MATCH}
    Then I must receive a password match error message

Scenario 04: Validate password change with wrong current password
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I enter wrong current password  ${INVALID_PASSWORD}  ${NEW_PASSWORD}  ${NEW_PASSWORD}
    Then I must receive a wrong current password error message

Scenario 05: Validate password change with invalid format
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I enter a password with invalid format  ${VALID_PASS_MORE_POCS}  ${PASSWORD_INVALID_FORMAT}  ${PASSWORD_INVALID_FORMAT}
    Then I must receive a password invalid format error message

Scenario 06: Validate password change with minimum length not reached
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I enter a password with invalid format  ${VALID_PASS_MORE_POCS}  ${PASSWORD_MINIMUM_LENGTH}  ${PASSWORD_MINIMUM_LENGTH}
    Then I must receive a password minimum length error message

Scenario 07: Account switch successfully
    [Tags]  high  las-automated-smoke-test  manage_account
    Given I have logged into the application
    When I switch my account
    Then I must be redirected to the other account