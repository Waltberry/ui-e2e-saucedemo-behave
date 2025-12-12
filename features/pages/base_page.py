from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

DEFAULT_TIMEOUT = 20

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_visible(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_clickable(self, by: By, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )

    # def click(self, by, locator, timeout=DEFAULT_TIMEOUT):
    #     elem = self.wait_clickable(by, locator, timeout)
    #     try:
    #         self.scroll_into_view(elem)
    #         elem.click()
    #     except Exception:
    #         self.js_click(elem)
            
    def click(self, by, locator, timeout=DEFAULT_TIMEOUT, attempts=2):
        last = None
        for _ in range(attempts):
            try:
                elem = self.wait_clickable(by, locator, timeout)
                self.scroll_into_view(elem)
                try:
                    elem.click()
                except Exception:
                    self.js_click(elem)
                return
            except (TimeoutException, ElementClickInterceptedException) as e:
                last = e
        raise last

    # def type(self, by, locator, text, timeout=DEFAULT_TIMEOUT):
    #     elem = self.wait_visible(by, locator, timeout)
    #     self.scroll_into_view(elem)
    #     elem.clear()
    #     elem.send_keys(text)
    
    def type(self, by, locator, text, timeout=DEFAULT_TIMEOUT, attempts=2):
        last = None
        for _ in range(attempts):
            try:
                elem = self.wait_visible(by, locator, timeout)
                self.scroll_into_view(elem)
                elem.clear()
                elem.send_keys(text)
                return
            except TimeoutException as e:
                last = e
        raise last

    # Helpers for stubborn elements in headless runs
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
        
    def wait_url_contains(self, fragment: str, timeout: int = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
        
    def wait_text_in(self, by, locator, text, timeout: int = DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((by, locator), text)
        )

