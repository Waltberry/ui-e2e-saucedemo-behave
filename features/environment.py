# features/environment.py
import os
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

SCREEN_DIR = pathlib.Path("artifacts") / "screenshots"
REPORT_DIR = pathlib.Path("reports") / "junit"



def before_all(context):
    # Ensure artifact folders exist
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Headless toggle (default: true)
    headless = os.getenv("HEADLESS", "true").lower() != "false"

    options = Options()
    if headless:
        # Chrome new headless mode
        options.add_argument("--headless=new")
    # CI hardening
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    if os.name == "nt":
        # Windows-specific options
        options.add_argument("--disable-gpu")

    # If GitHub action sets CHROME_PATH/CHROME_BIN, honor it
    chrome_bin = os.getenv("CHROME_PATH") or os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(0)  # we prefer explicit waits in page objects
    context.base_url = "https://www.saucedemo.com/"

# def after_step(context, step):
#     if step.status == "failed":
#         ts = time.strftime("%Y%m%d-%H%M%S")
#         safe_name = f"{context.scenario.name}__{step.name}".replace(" ", "_").replace("/", "_")
#         filepath = SCREEN_DIR / f"{safe_name}__{ts}.png"
#         try:
#             context.driver.save_screenshot(str(filepath))
#         except Exception:
#             pass  # don't block 
        
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
