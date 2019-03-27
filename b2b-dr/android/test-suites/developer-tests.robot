*** Settings ***

Documentation     Test suite intent to development of automated tests. Use it to make simple keyword tests.

Resource          ${CURDIR}/../keywords/libraries.robot
Resource          ${CURDIR}/../keywords/common.robot
Resource          ${CURDIR}/../variables/variables-global.robot

Library           ${CURDIR}/../variables/MyModule.py                                                           WITH NAME    myLib

Suite Setup       Bootstrap test environment
Suite Teardown    Shutdown test environment


*** Test Cases ***

Scenario: My Test
    [Tags]                      test
    [Setup]                     Launch application
    [Teardown]                  Exit application
    I select the environment    PreProd
    I select the environment    PreProd
    I select the environment    Dev
    I select the environment    Qa
    I select the environment    Dev
    I select the environment    PreProd
    I select the environment    Prod
    I select the environment    Qa
    I select the environment    PreProd
    I select the environment    PreProd
    I select the environment    Dev
    I select the environment    Qa
    I select the environment    Dev
    I select the environment    PreProd
    I select the environment    Prod
    I select the environment    Qa
    I select the environment    PreProd
    I select the environment    PreProd
    I select the environment    Dev
    I select the environment    Qa
    I select the environment    Dev
    I select the environment    PreProd
    I select the environment    Prod
    I select the environment    Qa

    #Test Me

*** Keywords ***

Test Me
    ${message}                  myLib.My Keyword         abc
    std.Log                     ${message}               console=yes
    ${message}                  myLib.Another            xyz
    std.Log                     ${message}               console=yes
    ${message}                  myLib.Another Keyword    jws
    std.Log                     ${message}               console=yes