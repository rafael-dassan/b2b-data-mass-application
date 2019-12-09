#language: en
@android
Feature: Beer Tech - Orders

@orders
Scenario: Buy a product
    Given that I have one or more products into my cart
    When I click on the Confirmar Pedido button
    Then the order must be completed