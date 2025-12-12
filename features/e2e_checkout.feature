Feature: E2E checkout on SauceDemo
  As a buyer on the demo store
  I want to log in, add an item, and complete checkout
  So that I see an order confirmation

  Scenario: Login → add to cart → checkout → confirm
    Given I open the SauceDemo app
    When I log in with standard credentials
    And I add "Sauce Labs Backpack" to the cart
    And I proceed to checkout
    And I enter checkout info "Onyero" "Ofuzim" "T3C2Y8"
    And I finish checkout
    Then I should see an order confirmation