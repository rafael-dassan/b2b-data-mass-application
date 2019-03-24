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
    When I login with my user credentials                      110918@mailinator.com                     Teste123
    Then I should be redirected to the home screen

Login Unsuccessfully With Invalid Credentials
    [Tags]                                                     basic
    Given I am on the login page
    When I login with invalid user credentials                 12345@mailinator.com                      12345
    Then I should see the invalid credentials error message

Login Unsuccessfully With Empty Credentials
    [Tags]                                                     basic
    Given I am on the login page
    When I login with empty user credentials                   ${EMPTY}                                  ${EMPTY}
    Then I should see the empty credentials error messages

Login Unsuccessfully With Invalid Email
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Credentials
    110934@mailinator.com                                      Teste123

Login Unsuccessfully With Invalid Password
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Credentials
    110918@mailinator.com                                      Teste12345

Login Unsuccessfully With Empty Email
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Empty Credentials
    ${EMPTY}                                                   Teste123

Login Unsuccessfully With Empty Password
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Empty Credentials
    110918@mailinator.com                                      ${EMPTY}

Login Unsuccessfully With Invalid Email Format
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Email Format
    invalid                                                    Teste123