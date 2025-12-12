from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    USER = (By.ID, "user-name")
    PASS = (By.ID, "password")
    BTN  = (By.ID, "login-button")
    ERROR= (By.CSS_SELECTOR, "h3[data-test='error']")

    def open_login(self):
        self.open("")

    def login(self, username, password):
        self.type(self.USER, username)
        self.type(self.PASS, password)
        self.click(self.BTN)

    def error_message(self):
        return self.text_of(self.ERROR)