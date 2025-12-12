from selenium.webdriver.common.by import By
from .base_page import BasePage

class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, "h2.complete-header")

    def is_complete(self) -> bool:
        try:
            el = self.wait_visible(*self.COMPLETE_HEADER)
            return "Thank you for your order!" in el.text
        except Exception:
            return False
