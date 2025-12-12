import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Global configuration defaults
BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com/")
HEADLESS = os.environ.get("HEADLESS", "1") != "0"
SCREENSHOT_DIR = Path(os.environ.get("SCREENSHOT_DIR", "reports/screenshots"))
FLAKY_RETRIES = int(os.environ.get("FLAKY_RETRIES", "2"))

def _mk_driver():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    # Selenium Manager will auto-provision chromedriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(0)
    return driver

def before_all(context):
    context.base_url = BASE_URL
    context.headless = HEADLESS
    context.screenshot_dir = SCREENSHOT_DIR
    context.flaky_retries = FLAKY_RETRIES
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def before_scenario(context, scenario):
    context.driver = _mk_driver()

def after_step(context, step):
    # On failure, take a screenshot.
    if step.status == "failed":
        ts = time.strftime("%Y%m%d-%H%M%S")
        name = f"{ts}_{step.name.replace(' ', '_')}.png"
        path = context.screenshot_dir / name
        try:
            context.driver.save_screenshot(str(path))
        except Exception:
            pass  # ignore if driver already gone

def after_scenario(context, scenario):
    # Always try to save a final screenshot (useful for CI artifacts).
    ts = time.strftime("%Y%m%d-%H%M%S")
    name = f"{ts}_{scenario.name.replace(' ', '_')}_final.png"
    path = context.screenshot_dir / name
    try:
        context.driver.save_screenshot(str(path))
    except Exception:
        pass
    try:
        context.driver.quit()
    except Exception:
        pass