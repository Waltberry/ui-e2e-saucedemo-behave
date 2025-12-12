from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

DEFAULT_TIMEOUT = 15

class BasePage:
    def __init__(self, driver, base_url=None, retries=2):
        self.driver = driver
        self.base_url = base_url or ""
        self.retries = retries

    def open(self, path=""):
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    def wait_for_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        last_err = None
        for _ in range(self.retries + 1):
            try:
                el = self.wait_for_clickable(locator, timeout)
                el.click()
                return
            except Exception as e:
                last_err = e
        raise last_err

    def type(self, locator, text, timeout=DEFAULT_TIMEOUT, clear=True):
        last_err = None
        for _ in range(self.retries + 1):
            try:
                el = self.wait_for_visible(locator, timeout)
                if clear:
                    el.clear()
                el.send_keys(text)
                return
            except Exception as e:
                last_err = e
        raise last_err

    def text_of(self, locator, timeout=DEFAULT_TIMEOUT):
        el = self.wait_for_visible(locator, timeout)
        return el.text.strip()

    def all_texts(self, locator, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )
        return [e.text.strip() for e in self.driver.find_elements(*locator)]