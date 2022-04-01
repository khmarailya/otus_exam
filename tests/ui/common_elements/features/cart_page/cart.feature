@ui
Feature: Cart page / Check Cart
  I want to check Cart on Cart page

  Background:
    Given I go to Cart page

  @smoke
  Scenario: Check Cart exists
    Then I see Chopping Cart in top
    And I see Cart button in header

  Scenario: Check empty Cart message
    When Cart is empty
    And I click on Cart
    Then I see Cart message "Your shopping cart is empty!"

  Scenario: Check go to Cart page
    When I click on Chopping Cart
    Then I go to Cart page

