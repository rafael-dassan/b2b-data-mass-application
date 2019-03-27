*** Settings ***
Documentation     Test scenarios to validate the creation of a new user with valid e-mail, validation of the message when the e-mail already exists, validation of the e-mail field and confirmation of the e-mail.
Suite Setup       Bootstrap test environment
Suite Teardown    Shutdown test environment
Test Setup        Launch application
Test Teardown     Exit application
Resource          ${CURDIR}/../keywords/register-new-account.robot
Force Tags        Register New Account


*** Test Cases ***
Scenario: Register using a new e-mail address
    [Documentation]                                                       Register using a new e-mail address
    [Tags]                                                                Basic
    Given I select the environment                                        Qa
    And I go to the register screen
    And I input personal information                                      John
    ...                                                                   Doe
    And I input an email address that has never been used before

    And I input confirmation email address

    And I input a Cell Phone Number
    ...                                                                   19777654443
    And I go to the next registration step 1
    And I input my account                                                582338
    ...                                                                   WCP/002312
    And I go to the next registration step 2

    Then I confirm that I want to register


Scenario: Fail to register (E-mail already registered)
    [Documentation]                                                       Fail to register
    [Tags]                                                                Alternative
    Given I select the environment                                        Qa
    And I go to the register screen
    And I input personal information
    ...                                                                   John
    ...                                                                   Doe

    And I input email already registered before
    ...                                                                   johndoe@gmail.com
    ...                                                                   johndoe@gmail.com

    And I input a Cell Phone Number
    ...                                                                   19777654443

    And I go to the next registration step 1
    And I input my account
    ...                                                                   582338
    ...                                                                   WCP/002312

    And I go to the next registration step 2

    Then I my account should not have been created


Scenario: Trying to register incorrectly filling the personal information page
    [Documentation]                                                       Trying to register incorrectly filling the personal information
    [Tags]                                                                Alternative
    Given I select the environment                                        Qa
    And I go to the register screen
    And I input personal information
    ...                                                                   John
    ...                                                                   Doe
    And I input email invalid
    ...                                                                   XXXXX
    ...                                                                   XXXXX
    And I input a Cell Phone Number
    ...                                                                   19777654443
    And I click in ok button next invalid

    And I confirm email invalid

    Then I try to advance to my account data screen

Scenario: Trying to register incorrectly with confirmation e-mail not matching
    [Documentation]                                                       Trying to register incorrectly with confirmation e-mail not matching
    [Tags]                                                                Alternative
    Given I select the environment                                        Qa
    And I go to the register screen
    And I input personal information
    ...                                                                   John
    ...                                                                   Doe
    And I input email invalid
    ...                                                                   johndoe@ciandt.com
    ...                                                                   john@ciandt.com
    And I input a Cell Phone Number
    ...                                                                   19777654443
    And I click in ok button next invalid

    And I confirm email invalid

    Then I try to advance to my account data screen error confirmation
