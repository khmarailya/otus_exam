@ui
Feature: Contacts page / Check Contacts
  I want to check Contacts on Contacts page

  Background:
    Given I go to Contacts page

  @smoke
  Scenario: Check Contacts exists
    Then I see Contacts in top
    And I see Contacts in footer

  Scenario: Check going to Contacts page from top
    When I click on Contacts in top
    Then I go to Contacts page

  Scenario: Check going to Contacts page from footer
    When I click on Contacts in footer
    Then I go to Contacts page
