#language: en
@android
Feature: Beer Tech - Login

@select_environment
Scenario: Select to the environment
    Given I am on Initial screen
    When I selected the enviroment "QA"
    Then I go to screen login

@login
Scenario: Login to the customer account
    Given that I have an existing account
    When I insert my credentials "REPUBLICADOMINICANA"
    When I click on the login button
    Then I must be logged successfully