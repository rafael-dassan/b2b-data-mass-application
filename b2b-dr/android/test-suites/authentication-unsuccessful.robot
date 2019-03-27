*** Settings ***

Documentation                          Unsuccessful Authentication Tests Suite

Resource                               ${CURDIR}/../keywords/authentication-unsuccessful.robot


Suite Setup
...                                    Run Keywords
...                                    Bootstrap test environment
...                                    AND
...                                    I have selected an environment and I go to authentication screen
...                                    Qa

Suite Teardown
...                                    Run Keywords
...                                    Shutdown test environment
...                                    AND
...                                    Exit application

Test Template                          Unsuccessful login

*** Test Cases ***

Scenario: Invalid user                 invalid                                                             
    ...                                Teste123
    [Tags]                             Alternative
Scenario: Invalid password             ahardinger@somethingdigital.com                                               
    ...                                12345678
    [Tags]                             Alternative
Scenario: Invalid user and password    invalid                                                             
    ...                                12345678
    [Tags]                             Alternative
Scenario: Empty user                   ${EMPTY}                                                            
    ...                                12345678
    [Tags]                             Alternative
    [Template]    Login action disabled
Scenario: Empty password               ahardinger@somethingdigital.com                                               
    ...                                ${EMPTY}
    [Template]    Login action disabled
    [Tags]                             Alternative


