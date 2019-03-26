*** Settings ***
Documentation              Authentication Test Suite
Resource                   ${CURDIR}/../keywords/common.robot
Resource                   ${CURDIR}/../keywords/authentication.robot
Test Setup                 Begin Web Test
Test Teardown              End Web Test

*** Variable ***
${VALID_EMAIL}             110918@mailinator.com
${VALID_PASSWORD}          Teste123
${INVALID_EMAIL}           12345@mailinator.com
${INVALID_PASSWORD}        12345
${INVALID_EMAIL_FORMAT}    invalid

*** Test Case ***
Login Successfully
    [Tags]                                                     basic
    Given I am on the login page
    When I login with my user credentials                      ${VALID_EMAIL}
    ...                                                        ${VALID_PASSWORD}
    Then I should be redirected to the home screen

Login Unsuccessfully With Invalid Credentials
    [Tags]                                                     basic
    Given I am on the login page
    When I login with invalid user credentials                 ${INVALID_EMAIL}
    ...                                                        ${INVALID_PASSWORD}
    Then I should see the invalid credentials error message

Login Unsuccessfully With Empty Credentials
    [Tags]                                                     basic
    Given I am on the login page
    When I login with empty user credentials                   ${EMPTY}
    ...                                                        ${EMPTY}
    Then I should see the empty credentials error messages

Login Unsuccessfully With Invalid Email
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Credentials
    ${INVALID_EMAIL}                                           ${VALID_PASSWORD}

Login Unsuccessfully With Invalid Password
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Credentials
    ${VALID_EMAIL}                                             ${INVALID_PASSWORD}

Login Unsuccessfully With Empty Email
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Empty Credentials
    ${EMPTY}                                                   ${VALID_PASSWORD}

Login Unsuccessfully With Empty Password
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Empty Credentials
    ${VALID_EMAIL}                                             ${EMPTY}

Login Unsuccessfully With Invalid Email Format
    [Tags]                                                     alternative
    [Template]                                                 Unsucessful Login Invalid Email Format
    ${INVALID_EMAIL_FORMAT}                                    ${VALID_PASSWORD}