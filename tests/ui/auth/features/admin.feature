@ui @auth
Feature: Auth / Check Admin Auth
  I want to check Auth on Admin page

  Background:
    Given I go to Admin login page

  Scenario: Check correct Auth
    When I login as "user" with "bitnami"
    Then I go to Dashboard page

  Scenario Outline: Check not correct Auth
    When I login as "<user>" with "<password>"
    Then I stay on Admin login page
    And I see Alert "No match for Username and/or Password."
    Examples:
      | user  | password |
      | user_ | bitnami  |
      | user  | bitnami1 |

