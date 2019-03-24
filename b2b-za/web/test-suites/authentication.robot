*** Settings ***
Documentation    Authentication Test Suite
Resource         ${CURDIR}/../keywords/common.robot
Resource         ${CURDIR}/../keywords/authentication.robot
Test Setup       Begin Web Test
Test Teardown    End Web Test

*** Test Case ***
Login Successfully
    [Tags]                                                     basic
    Given I am on the login page
    When I login with my user credentials                      110918@mailinator.com    Teste123
    Then I should be redirected to the home screen

Login Unsuccessfully With Invalid Credentials
    [Tags]                                                     alternative
    Given I am on the login page
    When I login with invalid user credentials                 12345@mailinator.com     12345
    Then I should see the invalid credentials error message

Login Unsuccessfully With Empty Credentials
    [Tags]                                                     alternative
    Given I am on the login page
    When I login with empty user credentials                   ${EMPTY}                 ${EMPTY}
    Then I should see the empty credentials error messages