from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    CHECKOUT = (By.ID, "checkout")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Your Cart"

    def checkout(self):
        self.click(self.CHECKOUT)