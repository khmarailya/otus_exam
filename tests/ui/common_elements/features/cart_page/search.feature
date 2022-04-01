@ui
Feature: Cart page / Check Search
  I want to check Search on Cart page

  Background:
    Given I go to Cart page

  @smoke
  Scenario: Check Search exists
    Then I see Search input in header

  Scenario: Check going to Search page
    When I click on Search button
    Then I go to Search page
