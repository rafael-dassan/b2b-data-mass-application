#language: en
@android
Feature: Beer Tech - Logout

@logout
Scenario: Logout to the customer account
    Given that I am logged
    When I click on the logout button
    Then I must be logged out