# features/pages/base_page.py
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = int(os.getenv("E2E_TIMEOUT", "15"))

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # ---- waits ----
    def wait_present(self, by, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_visible(self, by, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_clickable(self, by, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )

    def wait_url_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))

    def wait_until(self, predicate, timeout=DEFAULT_TIMEOUT, poll_frequency=0.2):
        """Poll a custom predicate until truthy."""
        return WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency).until(
            lambda d: predicate(d)
        )

    # ---- actions ----
    def click(self, by, locator, timeout=DEFAULT_TIMEOUT):
        """
        Resilient click: present -> scrollIntoView -> clickable -> click,
        fallbacks: ActionChains click, JS click. Retries a few times.
        """
        last = None
        for _ in range(3):
            elem = None
            try:
                elem = self.wait_present(by, locator, timeout)
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", elem
                    )
                except Exception:
                    pass

                elem = self.wait_clickable(by, locator, min(timeout, 10))
                elem.click()
                return
            except Exception as e:
                last = e
                try:
                    if elem:
                        ActionChains(self.driver).move_to_element(elem).click().perform()
                        return
                except Exception:
                    pass
                try:
                    if elem:
                        self.driver.execute_script("arguments[0].click();", elem)
                        return
                except Exception:
                    pass
                time.sleep(0.5)
        raise last

    def _ensure_value(self, elem, expected, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: elem.get_attribute("value") == expected
            )
        except Exception:
            # Fallback: set via JS and fire input/change (some headless runs miss keystrokes)
            self.driver.execute_script(
                """
                const el = arguments[0], val = arguments[1];
                el.value = val;
                el.dispatchEvent(new Event('input', {bubbles:true}));
                el.dispatchEvent(new Event('change', {bubbles:true}));
                """,
                elem, expected
            )

    def type(self, by, locator, text, timeout=DEFAULT_TIMEOUT):
        elem = self.wait_visible(by, locator, timeout)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elem)
        except Exception:
            pass
        elem.clear()
        elem.send_keys(text)
        self._ensure_value(elem, text, timeout=min(timeout, 5))
