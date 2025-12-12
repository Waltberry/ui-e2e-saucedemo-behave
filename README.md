![CI](https://github.com/Waltberry/ui-e2e-saucedemo-behave/actions/workflows/ci.yml/badge.svg)

# UI E2E — SauceDemo (Behave + Selenium)

A small, production-style end-to-end test suite that automates a purchase on the public **Sauce Demo** site.

**Flow covered:** login → add “Sauce Labs Backpack” to cart → cart → checkout info → overview → finish  
**Stack:** Python · Selenium WebDriver · Behave (Gherkin) · Page Object Model (POM) · GitHub Actions (Chrome)

---

## Why this project exists

**Quality Engineering** in a realistic, reproducible way:

- **Clear business flow** (buy a product) expressed in a single, readable **Gherkin** scenario.
- **Maintainable code** via **Page Object Model** and explicit waits (flakiness control).
- **CI-ready**: headless Chrome in GitHub Actions on Linux/Windows, with **JUnit XML** and **screenshots** on failure.
- **Minimal dependencies** and **no secrets** (public demo site, standard creds).

---

## What the project does

- Validates the **happy path checkout** on https://www.saucedemo.com/
- Uses **standard_user / secret_sauce** test account (public demo credentials).
- Persists **JUnit test reports** and failure **screenshots** as build artifacts.
- Supports **headless** (default) and **visible** browser runs.

---

## Design & reasoning

### Test approach

- **Behavior first**: a single, high-signal scenario that exercises the full user journey and multiple app layers (auth, inventory, cart, checkout).
- **Assertions at key checkpoints** only (inventory visible, item in cart, “Thank you” page) — avoids brittle micro-assertions.
- **Explicit waits** over implicit waits to reduce race conditions and clarify timing assumptions.
- **Tiny retry wrappers** for click/type to mitigate transient UI states without hiding legit failures.

### Architecture

- **Page Object Model (POM)** to encapsulate locators and interactions per page.
- **Behave step definitions** delegate to pages; Gherkin stays readable and business-focused.
- **`environment.py`** centralizes driver lifecycle, headless toggle, artifacts folder creation.

features/
checkout.feature             # Behavior (Gherkin)
steps/checkout_steps.py      # Glue: steps → page objects
pages/                       # POM: Login/Inventory/Cart/Checkout/Complete
environment.py               # WebDriver setup, screenshots, base_url
reports/junit/                 # JUnit XML (CI)
artifacts/screenshots/         # Screenshots on failure
.github/workflows/ci.yml       # GitHub Actions (Chrome on Linux/Windows)

### Reliability choices

- **Explicit waits** everywhere; **no implicit wait** (set to 0) to avoid hidden timing.
- **Scroll + JS-click fallback** where needed (e.g., element overlapped).
- **Headless by default** for CI determinism; local visible runs supported.

---

## SDLC notes (how this was built)

1. **Plan**: pick a stable public target (SauceDemo), define a single “purchase” scenario with clear acceptance criteria.
2. **Design**: choose POM + Behave; list pages & locators; decide on artifact outputs (JUnit, screenshots).
3. **Implement**: page objects → steps → feature; add waits, small retries; parameterize headless.
4. **Hardening**: add JUnit config, CI pipeline, artifacts upload, cross-OS matrix.
5. **Documentation**: this README + comments in code.
6. **Extend** (optional): negative tests (locked user), more products, sorting/cart removal, etc.

---

## Getting started

### Requirements
- Python 3.11+
- Chrome (local runs) — CI installs Chrome automatically

### Install & run (Windows PowerShell)
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Headless (default)
behave -f progress2

# Visible browser
$env:HEADLESS = "false"
behave -f progress2
````

**Artifacts after a run**

* JUnit XML → `reports/junit/`
* Failure screenshots → `artifacts/screenshots/`

---

## CI/CD

GitHub Actions workflow: `.github/workflows/ci.yml`

* Installs Python & Chrome
* Runs Behave headless
* Uploads **JUnit** and **screenshots** artifacts
* Matrix: `ubuntu-latest` and `windows-latest`

---

## Project structure

```
.
├─ behave.ini                        # JUnit config (reports/junit)
├─ requirements.txt                  # selenium, behave
├─ .github/workflows/ci.yml          # CI pipeline
├─ artifacts/screenshots/            # failure screenshots
├─ reports/junit/                    # JUnit XML
└─ features
   ├─ checkout.feature               # Gherkin scenario
   ├─ environment.py                 # driver lifecycle, headless, screenshots
   ├─ steps/checkout_steps.py        # step definitions
   └─ pages/
      ├─ base_page.py                # waits, click/type (with small retry)
      ├─ login_page.py
      ├─ inventory_page.py
      ├─ cart_page.py
      ├─ checkout_page.py
      └─ checkout_complete_page.py
```

---

## Feature (Gherkin)

```gherkin

Feature: Checkout flow on Sauce Demo
  As a customer
  I want to log in, add an item, and complete checkout
  So that I can see a confirmation

  Scenario: Login and purchase Sauce Labs Backpack
    Given I open the Saucedemo login page
    When I log in as "standard_user" with password "secret_sauce"
    And I add "Sauce Labs Backpack" to the cart
    And I proceed to checkout with "Onyero" "Ofuzim" "T3C2Y8"
    Then I should see the order confirmation

```

---

## Extending the suite

* **Negative login**: locked out user → error banner
* **Inventory sorting**: sort by price low→high → first/last price assertions
* **Cart quantity/remove**: add/remove and verify totals
* **Visual checkpoint** (lightweight): assert stable texts/labels, not pixels

Each new behavior = new `.feature` + page methods + steps. Keep assertions **high value** and **resilient**.
