*** Settings ***
Documentation      Segment for Order Transparency Feature.
#Suite Setup       Bootstrap test environment
#Suite Teardown    Shutdown test environment
Test Setup         Run Keywords                                              I am authenticated    AND    I go to My Account screen
#Test Teardown     Exit application
Resource           ${CURDIR}/../keywords/segment-order-transparency.robot

*** Test Cases ***
Scenario: Upcoming Delivery Viewed
    [Documentation]
    [Tags]                                                         Segment    Order Transparency
    Given I am on My Account screen
    When I click on "orders" tab
    Then I validate the sent segment event on analytics console