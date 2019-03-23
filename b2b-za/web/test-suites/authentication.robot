*** Settings ***
Documentation   Authentication Test Suite
Resource        ${CURDIR}/../keywords/common.robot
Resource        ${CURDIR}/../keywords/authentication.robot
Resource        ${CURDIR}/../variables/variables.robot
Test Setup      Begin Web Test
Test Teardown   End Web Test

*** Test Case ***
Login Successfully
    Given I am on the login page
    When I login with my user credentials                   110918@mailinator.com   Teste123    
    Then I should be redirected to the home screen

Login Unsucessfully For Empty Credentials
    Given I am on the login page
    When I try to login with empty credentials              ${EMPTY}    ${EMPTY}    
    Then I should see empty credentials error messages

Login Unsucessfully For Empty User
    Given I am on the login page
    When I try to login with empty email                    ${EMPTY}    Teste123      
    Then I should see an empty email error message

Login Unsucessfully For Empty Password
    Given I am on the login page
    When I try to login with empty password                 110918@mailinator.com   ${EMPTY}      
    Then I should see an empty password error message