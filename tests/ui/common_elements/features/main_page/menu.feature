@ui
Feature: Main page / Check Menu
  I want to check Menu on Main page

  Background:
    Given I go to Main page

  @smoke
  Scenario: Check Menu exists
    Then I see Menu with "8" items

  Scenario Outline: Check Menu items and going to Catalogue page
    When I click on Menu item "<title>"
    Then I see Menu sub item "Show All <title>"
    When I click on Menu sub item
    Then I go to Catalogue page "<title>"
    Examples:
      | title               |
      | Desktops            |
      | Laptops & Notebooks |
      | Components          |

