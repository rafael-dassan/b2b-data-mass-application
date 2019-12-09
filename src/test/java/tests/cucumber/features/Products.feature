#language: en
@android
Feature: Beer Tech - Products

@products
Scenario: Insert products into the cart
    Given that I want to buy some products
    When I select one or more products
    Then the products must be added into my cart