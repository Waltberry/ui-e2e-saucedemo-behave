from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "span.title")
    CART_BADGE = (By.CSS_SELECTOR, "span.shopping_cart_badge")
    CART_LINK  = (By.ID, "shopping_cart_container")

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Products"

    def add_item(self, item_name):
        # Buttons have id like: add-to-cart-sauce-labs-backpack
        slug = item_name.lower().replace(" ", "-")
        btn = (By.ID, f"add-to-cart-{slug}")
        self.click(btn)

    def go_to_cart(self):
        self.click(self.CART_LINK)