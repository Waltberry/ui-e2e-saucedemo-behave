from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutOverviewPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    FINISH= (By.ID, "finish")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Checkout: Overview"

    def finish(self):
        self.click(self.FINISH)