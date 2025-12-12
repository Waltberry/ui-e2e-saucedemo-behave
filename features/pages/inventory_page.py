from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")

    def add_item_to_cart(self, item_name: str):
        # "add-to-cart-sauce-labs-backpack"
        slug = item_name.lower().replace(" ", "-")
        btn_id = f"add-to-cart-{slug}"
        self.click(By.ID, btn_id)

    def go_to_cart(self):
        self.click(*self.CART_LINK)
