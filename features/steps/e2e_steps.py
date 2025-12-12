from behave import given, when, then
from selenium.webdriver.common.by import By
from ..pages.login_page import LoginPage
from ..pages.inventory_page import InventoryPage
from ..pages.cart_page import CartPage
from ..pages.checkout_info_page import CheckoutInfoPage
from ..pages.checkout_overview_page import CheckoutOverviewPage
from ..pages.checkout_complete_page import CheckoutCompletePage

STANDARD_USER = ("standard_user", "secret_sauce")

@given("I open the SauceDemo app")
def step_open(context):
    context.login = LoginPage(context.driver, base_url=context.base_url, retries=context.flaky_retries)
    context.login.open_login()

@when("I log in with standard credentials")
def step_login(context):
    user, pwd = STANDARD_USER
    context.login.login(user, pwd)
    context.inventory = InventoryPage(context.driver, base_url=context.base_url, retries=context.flaky_retries)
    assert context.inventory.is_loaded()

@when('I add "{item}" to the cart')
def step_add_item(context, item):
    context.inventory.add_item(item)

@when("I proceed to checkout")
def step_checkout(context):
    context.inventory.go_to_cart()
    context.cart = CartPage(context.driver, base_url=context.base_url, retries=context.flaky_retries)
    assert context.cart.is_loaded()
    context.cart.checkout()
    context.info = CheckoutInfoPage(context.driver, base_url=context.base_url, retries=context.flaky_retries)
    assert context.info.is_loaded()

@when('I enter checkout info "{first}" "{last}" "{postal}"')
def step_enter_info(context, first, last, postal):
    context.info.fill_info(first, last, postal)
    context.overview = CheckoutOverviewPage(context.driver, base_url=context.base_url, retries=context.flaky_retries)
    assert context.overview.is_loaded()

@when("I finish checkout")
def step_finish(context):
    context.overview.finish()
    context.complete = CheckoutCompletePage(context.driver, base_url=context.base_url, retries=context.flaky_retries)

@then("I should see an order confirmation")
def step_confirm(context):
    assert context.complete.is_loaded()
    assert "THANK YOU FOR YOUR ORDER" in context.complete.confirmation_text().upper()