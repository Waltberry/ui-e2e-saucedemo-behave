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

    def _ensure_on_step_one(self, timeout):
        # Prefer element presence (more reliable than URL-only)
        if self.wait_until(lambda d: len(d.find_elements(*self.FIRST)) > 0, timeout=timeout):
            return
        # If element isn't visible yet, accept URL or hard-navigate
        if not self.wait_until(lambda d: self.STEP_ONE_URL in d.current_url, timeout=timeout):
            try:
                current = self.driver.current_url
                parts = current.split("/")
                origin = f"{parts[0]}//{parts[2]}"
                self.driver.get(f"{origin}/checkout-step-one.html")
            except Exception:
                self.driver.get("https://www.saucedemo.com/checkout-step-one.html")
        self.wait_present(*self.FIRST, timeout=timeout)

    def fill_info(self, first: str, last: str, postal: str, timeout: int = 25):
        self._ensure_on_step_one(timeout)
        # Make sure keystrokes stick; fallback to JS if needed
        self.set_value(*self.FIRST, first, timeout=timeout)
        self.set_value(*self.LAST,  last,  timeout=timeout)
        self.set_value(*self.POSTAL, postal, timeout=timeout)

    def _await_overview_or_error(self, timeout):
        WebDriverWait(self.driver, timeout).until(EC.any_of(
            EC.url_contains(self.STEP_TWO_URL),
            EC.presence_of_element_located(self.FINISH),
            EC.presence_of_element_located(self.ERROR)
        ))

    def continue_to_overview(self, timeout: int = 25):
        self.click(*self.CONTINUE, timeout=timeout)
        try:
            self._await_overview_or_error(timeout)
        except Exception:
            # One retry for headless/Windows flake
            self.click(*self.CONTINUE, timeout=timeout)
            self._await_overview_or_error(max(timeout, 30))
        errs = self.driver.find_elements(*self.ERROR)
        if errs:
            raise AssertionError(f"Checkout validation error: {errs[0].text}")

    def finish(self, timeout: int = 25):
        self.click(*self.FINISH, timeout=timeout)
