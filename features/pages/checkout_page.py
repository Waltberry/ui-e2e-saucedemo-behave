# features/pages/checkout_page.py
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
    COMPLETE_URL  = "checkout-complete"
    COMPLETE_HDR  = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first: str, last: str, postal: str, timeout: int = 25):
        # Ensure we are on the form page (slow headless sometimes lags)
        self.wait_url_contains(self.STEP_ONE_URL, timeout=timeout)
        self.type(*self.FIRST, first)
        self.type(*self.LAST, last)
        self.type(*self.POSTAL, postal)

    def _await_overview_or_error(self, timeout):
        WebDriverWait(self.driver, timeout).until(EC.any_of(
            EC.url_contains(self.STEP_TWO_URL),
            EC.presence_of_element_located(self.FINISH),
            EC.presence_of_element_located(self.ERROR),
        ))

    def continue_to_overview(self, timeout: int = 25):
        self.click(*self.CONTINUE, timeout=timeout)
        try:
            self._await_overview_or_error(timeout)
        except Exception:
            # Headless sometimes misses the click; verify fields still filled and try once more
            for by, loc in (self.FIRST, self.LAST, self.POSTAL):
                _ = self.wait_visible(by, loc, timeout=min(timeout, 5))
            self.click(*self.CONTINUE, timeout=timeout)
            self._await_overview_or_error(max(timeout, 45))

        errs = self.driver.find_elements(*self.ERROR)
        if errs:
            raise AssertionError(f"Checkout validation error: {errs[0].text}")

    def finish(self, timeout: int = 25):
        self.click(*self.FINISH, timeout=timeout)
        WebDriverWait(self.driver, max(timeout, 35)).until(EC.any_of(
            EC.url_contains(self.COMPLETE_URL),
            EC.visibility_of_element_located(self.COMPLETE_HDR),
            EC.presence_of_element_located(self.ERROR),
        ))
        errs = self.driver.find_elements(*self.ERROR)
        if errs:
            raise AssertionError(f"Checkout validation error: {errs[0].text}")
