*** Settings ***

Documentation     Registration-validation Tests Suite

Resource          ${CURDIR}/../keywords/initial-registration-validation.robot

Suite Setup       Bootstrap test environment
Suite Teardown    Shutdown test environment

Test Setup        Launch application
Test Teardown     Exit application

*** Test Cases ***

Scenario: Validating initial registration screen dialogs
    [Tags]
    [Documentation]
    Given I select the environment                                                    Qa
    When I foward to initial registration validation screen
    Then I validate all dialogs contents in initial registration validation screen
