#language: en
@common @login
Feature: Login
    As a registered user in the app
    James would like to sign in to the app
    To access your store at any time

    Background:
        Given  that "James" as an "ADM" user is in the login screen


    Scenario: Valid Login
        And he filled in the login data correctly
        When he triggers the option to access
        Then the account list page should be displayed