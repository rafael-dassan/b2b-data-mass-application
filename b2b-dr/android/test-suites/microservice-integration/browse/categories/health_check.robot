*** Settings ***
Resource         ../../../../keywords/common.robot
Resource         ../../../../keywords/microservice-integration/browse/categories/categories_keywords.robot


Test Setup	Run Keywords    I open the app with login correct


*** Test Cases ***
Scenario: [Android] Health check categories - Verify display of a category, sub-category and item
    Given I Verify the screen is successfully loaded
    Then I select the first category
    And I select the first sub-category
    And I Verify items were successfully loaded

    [Teardown]	Exit application