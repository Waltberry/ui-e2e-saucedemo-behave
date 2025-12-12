from selenium.webdriver.common.by import By
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
        # Ensure we are on the form page in visible (slower) runs
        self.wait_url_contains(self.STEP_ONE_URL, timeout=timeout)
        self.type(*self.FIRST, first)
        self.type(*self.LAST, last)
        self.type(*self.POSTAL, postal)

    def continue_to_overview(self, timeout: int = 25):
        self.click(*self.CONTINUE, timeout=timeout)
        # Either URL advances to step-two or FINISH appears, or an error appears
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.STEP_TWO_URL in d.current_url
                      or len(d.find_elements(*self.FINISH)) > 0
                      or len(d.find_elements(*self.ERROR)) > 0
        )
        errs = self.driver.find_elements(*self.ERROR)
        if errs:
            raise AssertionError(f"Checkout validation error: {errs[0].text}")

    def finish(self, timeout: int = 25):
        self.click(*self.FINISH, timeout=timeout)
