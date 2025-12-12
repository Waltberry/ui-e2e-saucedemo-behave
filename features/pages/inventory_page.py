from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage, DEFAULT_TIMEOUT

class InventoryPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")

    def add_item_to_cart(self, item_name: str):
        slug = item_name.lower().replace(" ", "-")
        btn_id = f"add-to-cart-{slug}"
        self.click(By.ID, btn_id)

    def go_to_cart(self, timeout=DEFAULT_TIMEOUT):
        # Try click + wait twice, then hard-navigate.
        for _ in range(2):
            self.click(*self.CART_LINK, timeout=timeout)
            ok = self.wait_until(
                lambda d: "/cart.html" in d.current_url or len(d.find_elements(By.ID, "checkout")) > 0,
                timeout=timeout
            )
            if ok:
                return
        try:
            # Build origin from current URL
            current = self.driver.current_url
            parts = current.split("/")
            origin = f"{parts[0]}//{parts[2]}"
            self.driver.get(f"{origin}/cart.html")
        except Exception:
            self.driver.get("https://www.saucedemo.com/cart.html")
        self.wait_present(By.ID, "checkout", timeout=timeout)
