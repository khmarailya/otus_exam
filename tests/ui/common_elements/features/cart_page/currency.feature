@ui
Feature: Cart page / Check Currency
  I want to check Currency on Cart page

  Background:
    Given I go to Cart page

  @smoke
  Scenario: Check currency exists
    Then I see Currency in top

  Scenario: Check currency list
    When I open Currency menu
    Then I see Currency list: € Euro, £ Pound Sterling, $ US Dollar

  Scenario Outline: Check currency change
    When I open Currency menu
    And I choose "<text>" as Currency
    Then Currency has sign "<sign>"
    And Cart has sign "<sign>"
    Examples:
      | text             | sign |
      | € Euro           | €    |
      | £ Pound Sterling | £    |
      | $ US Dollar      | $    |

