from selenium.webdriver.common.by import By
from .base_page import BasePage, DEFAULT_TIMEOUT

class InventoryPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")

    def add_item_to_cart(self, item_name: str):
        slug = item_name.lower().replace(" ", "-")
        btn_id = f"add-to-cart-{slug}"
        self.click(By.ID, btn_id)

    def go_to_cart(self, timeout=DEFAULT_TIMEOUT):
        # Try click+wait twice (Windows CI can be slow to navigate)
        for _ in range(2):
            self.click(*self.CART_LINK, timeout=timeout)
            if self.wait_until(
                lambda d: "/cart.html" in d.current_url
                          or len(d.find_elements(By.ID, "checkout")) > 0,
                timeout=timeout
            ):
                return
        # Last resort: direct navigation (stabilizes Windows headless)
        try:
            current = self.driver.current_url
            # derive origin to avoid hardcoding (https://host/tail)
            parts = current.split("/")
            origin = f"{parts[0]}//{parts[2]}"
            self.driver.get(f"{origin}/cart.html")
        except Exception:
            # absolute fallback if parsing fails
            self.driver.get("https://www.saucedemo.com/cart.html")
        # Ensure cart loaded
        self.wait_present(By.ID, "checkout", timeout=timeout)
