*** Settings ***
Resource         ../../../../keywords/common.robot
Resource         ../../../../keywords/microservice-integration/browse/categories/categories_keywords.robot
Resource         ../../../../keywords/microservice-integration/browse/promotions/promotions_keywords.robot


Test Setup	Run Keywords    I open the app with login correct


*** Test Cases ***
Scenario: [Android] Verify if promotion banner is correctly being displayed and can be slided
    Given I Verify the screen is successfully loaded
    Then I check there are banners
    And I am able to swipe over the banner

    [Teardown]	Exit application