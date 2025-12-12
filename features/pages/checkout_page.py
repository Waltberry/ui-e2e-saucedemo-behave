from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage, DEFAULT_TIMEOUT

class CheckoutPage(BasePage):
    FIRST   = (By.ID, "first-name")
    LAST    = (By.ID, "last-name")
    POSTAL  = (By.ID, "postal-code")
    CONTINUE= (By.ID, "continue")
    FINISH  = (By.ID, "finish")
    ERROR   = (By.CSS_SELECTOR, "h3[data-test='error']")
    STEP_ONE_URL  = "checkout-step-one"
    STEP_TWO_URL  = "checkout-step-two"

    def fill_info(self, first: str, last: str, postal: str, timeout: int = 25):
        self.wait_url_contains(self.STEP_ONE_URL, timeout=timeout)
        self.type(*self.FIRST, first)
        self.type(*self.LAST, last)
        self.type(*self.POSTAL, postal)

    def _await_overview_or_error(self, timeout):
        WebDriverWait(self.driver, timeout).until(EC.any_of(
            EC.url_contains(self.STEP_TWO_URL),
            EC.presence_of_element_located(self.FINISH),
            EC.presence_of_element_located(self.ERROR)
        ))

    def continue_to_overview(self, timeout: int = 25):
        # First attempt
        self.click(*self.CONTINUE, timeout=timeout)
        try:
            self._await_overview_or_error(timeout)
        except Exception:
            # One more click (headless Windows can occasionally ignore the first)
            self.click(*self.CONTINUE, timeout=timeout)
            self._await_overview_or_error(max(timeout, 30))

        errs = self.driver.find_elements(*self.ERROR)
        if errs:
            raise AssertionError(f"Checkout validation error: {errs[0].text}")

    def finish(self, timeout: int = 25):
        self.click(*self.FINISH, timeout=timeout)
