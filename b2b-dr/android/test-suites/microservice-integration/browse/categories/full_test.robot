*** Settings ***
Resource         ../../../../keywords/common.robot
Resource         ../../../../keywords/microservice-integration/browse/categories/categories_keywords.robot
Resource         ../../../../../microservice/CategoriesMicroservice.robot


Test Setup	Run Keywords    I open the app with login correct


*** Test Cases ***
Scenario: [Android] Verify all categories comparing with the Microservice
    Given I Verify the screen is successfully loaded
    Then I get categories from api
    And I compare with the categories shown

    [Teardown]	Exit application