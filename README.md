# UI E2E: Selenium + Behave (Gherkin) on SauceDemo

End-to-end checkout flow on the public **Swag Labs** demo store: https://www.saucedemo.com/  
Flow: **login → add to cart → checkout → confirm order**.

> This project is designed as a fast, portfolio‑ready automation suite with **page objects**, **screenshots on failure**, **headless mode**, **basic retries**, and **GitHub Actions** CI (with artifacts).

---

## SDLC at a glance
**Requirements → Test Plan → Design → Implementation → CI → Reporting → Next steps**

### 1) Requirements
- Validate a happy‑path purchase for a known product on a public demo store
- Run reliably locally and in CI (Ubuntu + Chrome), headless by default
- Save screenshots on failure; publish reports as CI artifacts

### 2) Test Plan (scope for v1)
- Browser: Chrome (headless by default)
- Data: built‑in Swag Labs creds (`standard_user` / `secret_sauce`)
- Scenario: login → add “Sauce Labs Backpack” → checkout → see confirmation
- Exit: “THANK YOU FOR YOUR ORDER!” appears on the final page

### 3) Design
- **Behave (Gherkin)** for readability
- **Page Object Model** (`features/pages/*`) for maintainability
- **Hooks** in `environment.py` for driver lifecycle, screenshots, config
- **Waits** (WebDriverWait) to reduce flakiness; simple wrapper retries

### 4) Implementation
- Single feature `e2e_checkout.feature`
- Step defs in `features/steps/e2e_steps.py`
- Page objects for key screens
- `HEADLESS=1` by default; set `HEADLESS=0` to see the browser
- `FLAKY_RETRIES=2` basic retries inside common actions

### 5) CI
- GitHub Actions workflow (`.github/workflows/ci.yml`)
- Sets up Python + Chrome; runs Behave headless
- Uploads logs, JUnit XML, and screenshots as artifacts

### 6) Reporting
- Console `progress` formatter + timings
- JUnit XML in `reports/junit/*` for CI
- Failure screenshots in `reports/screenshots/`

### 7) Next steps
- Add negative tests (bad login, inventory ordering)
- Parallelize by tags on a Selenium Grid (or Sauce Labs/BrowserStack)
- Add Allure or HTML reporting
- Expand data‑driven scenarios from an examples table

---

## Setup

```bash
# (Optional) create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Run locally

```bash
# Default: headless
behave

# See the browser:
HEADLESS=0 behave

# Save JUnit + progress logs explicitly:
behave -f progress -o reports/behave.log -f junit -o reports/junit
```

Artifacts:
- Screenshots on failure: `reports/screenshots/`
- Logs/JUnit: `reports/`

## GitHub Actions
A ready workflow at `.github/workflows/ci.yml` runs on every push/PR.
Artifacts are uploaded for download from the Actions run.

## Project tree

```
ui-e2e-saucedemo-behave/
├─ .github/workflows/ci.yml
├─ features/
│  ├─ e2e_checkout.feature
│  ├─ environment.py
│  ├─ pages/
│  │  ├─ base_page.py
│  │  ├─ login_page.py
│  │  ├─ inventory_page.py
│  │  ├─ cart_page.py
│  │  ├─ checkout_info_page.py
│  │  ├─ checkout_overview_page.py
│  │  └─ checkout_complete_page.py
│  └─ steps/
│     └─ e2e_steps.py
├─ scripts/run_behave.sh
├─ behave.ini
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## Public demo site
We use **Swag Labs** (Sauce Labs demo): https://www.saucedemo.com/  
Credentials (public): `standard_user` / `secret_sauce`

---

## Git commands (create your repo and push)

```bash
git init
git add .
git commit -m "chore: initial Selenium+Behave E2E on SauceDemo"

# Create GH repo (requires GitHub CLI 'gh' and that you're authenticated)
gh repo create ui-e2e-saucedemo-behave --public \
  --description "UI E2E checkout (Selenium+Behave) on SauceDemo: login → add cart → checkout → confirm"

git branch -M main
git remote add origin https://github.com/Waltberry/ui-e2e-saucedemo-behave.git
git remote -v
git push -u origin main
```