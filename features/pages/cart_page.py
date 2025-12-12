from selenium.webdriver.common.by import By
from .base_page import BasePage, DEFAULT_TIMEOUT

class CartPage(BasePage):
    CHECKOUT_BTN = (By.ID, "checkout")

    def click_checkout(self, timeout=DEFAULT_TIMEOUT):
        # CI can lag after clicking cart icon; confirm we are really on the cart page.
        self.wait_url_contains("/cart.html", timeout=timeout)
        self.click(*self.CHECKOUT_BTN, timeout=timeout)
