*** Settings ***
Resource         ../../../../keywords/common.robot
Resource         ../../../../keywords/microservice-integration/browse/categories/categories_keywords.robot
Resource         ../../../../keywords/microservice-integration/browse/combos/combos_keywords.robot


Test Setup	Run Keywords    I open the app with login correct


*** Test Cases ***
Scenario: [Android] Verify All Combos Comparing With the Microservice
    Given I Verify the screen is successfully loaded
    Then I select the combos menu
    And I verify the combos were successfully loaded
    And I get the information from the microservice
    And I compare the information shown with the information from the microservice

    [Teardown]	Exit application