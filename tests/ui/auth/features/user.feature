@ui @auth
Feature: Auth / Check User Register
  I want to check Register of new User on Register page

  Background:
    Given I go to Register page


  Scenario Outline: Check wrong password length
    When I set password with "<cnt>" chars
    And I continue
    Then I stay on Register page
    And I see password alert "Password must be between 4 and 20 characters!"
    Examples: empty
      | cnt |
      | 0   |
    Examples: less than border
      | cnt |
      | 3   |
    @xfail
    Examples: greater than border
      | cnt |
      | 21  |


  Scenario Outline: Check correct password length
    When I set password with "<cnt>" chars
    And I continue
    Then I stay on Register page
    And I do not see password alert
    Examples: equal to least border
      | cnt |
      | 4   |
    Examples: equal to greatest border
      | cnt |
      | 20  |


  Scenario: Wrong password confirm
    When I set password "1234"
    And I confirm password "1243"
    And I continue
    Then I stay on Register page
    And I see confirm alert "Password confirmation does not match password!"

  @xfail
  Scenario: Check success register (Issue: https changes to http after continue)
    When I set firstname "firstname"
    And I set lastname "lastname"
    And I set random email
    And I set random phone
    And I set password "123456"
    And I confirm password "123456"
    And I agree
    And I continue
    Then I go to Success Register page

