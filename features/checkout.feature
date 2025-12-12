Feature: Checkout flow on Sauce Demo
  As a customer
  I want to log in, add an item, and complete checkout
  So that I can see a confirmation

  Scenario: Login and purchase Sauce Labs Backpack
    Given I open the Saucedemo login page
    When I log in as "standard_user" with password "secret_sauce"
    And I add "Sauce Labs Backpack" to the cart
    And I proceed to checkout with "Onyero" "Ofuzim" "T3C2Y8"
    Then I should see the order confirmation
