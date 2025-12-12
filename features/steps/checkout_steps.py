from behave import given, when, then
from features.pages.login_page import LoginPage
from features.pages.inventory_page import InventoryPage
from features.pages.cart_page import CartPage
from features.pages.checkout_page import CheckoutPage
from features.pages.checkout_complete_page import CheckoutCompletePage

@given('I open the Saucedemo login page')
def step_open_login(context):
    context.login = LoginPage(context.driver, context.base_url)
    context.login.open()

@when('I log in as "{username}" with password "{password}"')
def step_login(context, username, password):
    context.login.login(username, password)
    context.inventory = InventoryPage(context.driver)

@when('I add "{item_name}" to the cart')
def step_add_item(context, item_name):
    context.inventory.add_item_to_cart(item_name)
    context.inventory.go_to_cart()
    context.cart = CartPage(context.driver)

@when('I proceed to checkout with "{first}" "{last}" "{postal}"')
def step_checkout(context, first, last, postal):
    context.cart.click_checkout()
    context.checkout = CheckoutPage(context.driver)
    context.checkout.fill_info(first, last, postal)
    context.checkout.continue_to_overview()
    context.checkout.finish()

@then('I should see the order confirmation')
def step_confirmation(context):
    done = CheckoutCompletePage(context.driver)
    assert done.is_complete(), "Order confirmation not shown"
