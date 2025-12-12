from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutInfoPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    FIRST = (By.ID, "first-name")
    LAST  = (By.ID, "last-name")
    POSTAL= (By.ID, "postal-code")
    CONT  = (By.ID, "continue")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Checkout: Your Information"

    def fill_info(self, first, last, postal):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.POSTAL, postal)
        self.click(self.CONT)