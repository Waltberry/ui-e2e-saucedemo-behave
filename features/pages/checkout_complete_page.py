from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    HEADER= (By.CSS_SELECTOR, "h2.complete-header")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Checkout: Complete!"

    def confirmation_text(self):
        return self.text_of(self.HEADER)