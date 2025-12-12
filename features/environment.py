# features/environment.py
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

SCREEN_DIR = pathlib.Path("artifacts") / "screenshots"
REPORT_DIR = pathlib.Path("reports") / "junit"

def before_all(context):
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    headless = os.getenv("HEADLESS", "true").lower() != "false"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")  # Windows headless stability
        options.add_argument("--hide-scrollbars")
    # CI hardening
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-extensions")
    options.add_argument("--mute-audio")

    # Honor Chrome path from the action
    chrome_bin = os.getenv("CHROME_PATH") or os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(0)
    context.base_url = "https://www.saucedemo.com/"

def after_step(context, step):
    if step.status == "failed" and hasattr(context, "driver"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.join("artifacts", "screenshots")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"failed_{ts}.png")
        try:
            context.driver.save_screenshot(path)
            print(f"\n[debug] Saved screenshot: {path}")
        except Exception as e:
            print(f"\n[debug] Failed to save screenshot: {e}")

def after_all(context):
    try:
        context.driver.quit()
    except Exception:
        pass
