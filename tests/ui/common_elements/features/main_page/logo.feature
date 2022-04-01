@ui
Feature: Main page / Check Logo
  I want to check Logo on Main page

  Background:
    Given I go to Main page

  @smoke
  Scenario: Check Logo exists
    Then I see Logo in header

  Scenario: Check going to Main page
    When I click on Logo
    Then I go to Main page
