from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage, DEFAULT_TIMEOUT

class CheckoutCompletePage(BasePage):
    URL_FRAGMENT   = "checkout-complete"
    COMPLETE_HDR   = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT  = (By.CLASS_NAME, "complete-text")
    BACK_BTN       = (By.ID, "back-to-products")

    def wait_complete(self, timeout=DEFAULT_TIMEOUT):
        """
        Wait until the order-complete page is loaded. Returns True if detected.
        """
        WebDriverWait(self.driver, timeout).until(EC.any_of(
            EC.url_contains(self.URL_FRAGMENT),
            EC.presence_of_element_located(self.COMPLETE_HDR),
            EC.presence_of_element_located(self.BACK_BTN),
        ))
        # Enforce a stable state: URL or header present
        return self.is_complete()

    def is_complete(self):
        return (
            self.URL_FRAGMENT in self.driver.current_url or
            len(self.driver.find_elements(*self.COMPLETE_HDR)) > 0 or
            len(self.driver.find_elements(*self.BACK_BTN)) > 0
        )
