*** Settings ***
Documentation     Authentication Tests Suite
Suite Setup       Bootstrap test environment
Suite Teardown    Shutdown test environment
Test Setup        Launch application
Test Teardown     Exit application
Resource          ../variables/variables-global.robot
Resource          ../keywords/common.robot
Resource          ../keywords/authentication.robot


*** Test Cases ***
Scenario: Login successfully as user with only one POC
    [Documentation]                                    Login successfuly as user with *only one POC* (Point of Consumption).
    [Tags]
    Given I select the environment                     Qa
    When I login with my user credentials              190319@mailinator.com                                                      Teste123
    And I navigate through all introduction screens
    Then I will be redirected to browse screen

Scenario: Login successfully as user with multiple POCs
    [Documentation]                                                Login successfuly as user with *multiple POCs* (Point of Consumption).
    [Tags]                                                         Basic
    Given I select the environment                                 Qa
    When I login with my user credentials                          ahardinger@somethingdigital.com                                                     pZhU6KckqNQTkPc
    And I choose the POC                                           0000100089
    And I navigate through all introduction screens
    Then I will be redirected to browse screen

Scenario: Contact customer service via the phone through the login page
    [Documentation]                                                Contact customer service via the phone
    [Tags]                                                         Basic
    Given I select the environment                                 Qa
    and I go from startup screen to authentication screen          ahardinger@somethingdigital.com                                                      pZhU6KckqNQTkPc
    When I click to contact the customer service through phone
    Then I see the phone application is opened

Scenario: Contact customer service via the email through the login page
    [Documentation]                                                Contact customer service via the email
    [Tags]                                                         Basic
    Given I select the environment                                 Qa
    and I go from startup screen to authentication screen          ahardinger@somethingdigital.com                                                      pZhU6KckqNQTkPc
    When I click to contact the customer service through e-mail
    Then I see the e-mail application is opened
