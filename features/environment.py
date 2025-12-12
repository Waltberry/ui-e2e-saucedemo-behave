import os, pathlib
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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-features=PushMessaging,BackgroundFetch,OptimizationHints")
    if os.name == "nt":
        options.add_argument("--disable-gpu")
    # Faster transitions; don’t wait for subresources
    options.page_load_strategy = "eager"

    chrome_bin = os.getenv("CHROME_PATH") or os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(0)
    context.base_url = "https://www.saucedemo.com/"

def after_step(context, step):
    if step.status == "failed" and hasattr(context, "driver"):
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_dir = os.path.join("artifacts", "screenshots")
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, f"failed_{ts}.png")
            context.driver.save_screenshot(path)
            print(f"\n[debug] Saved screenshot: {path}")
        except Exception as e:
            # Safety: ignore invalid session/DevTools disconnects
            print(f"\n[debug] Screenshot skipped: {e}")

def after_all(context):
    try:
        context.driver.quit()
    except Exception:
        pass
