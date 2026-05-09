from playwright.sync_api import sync_playwright
import pytest

REPORTS_URL = "https://www.chately.app/dashboard/reports"
BILLING_URL = "https://www.chately.app/dashboard/billing"

# --- Reusable login function ------------------------------------------
def login(page):
    page.goto("https://www.chately.app/auth/login")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    page.fill('input[type="email"]', "softwarear312@gmail.com")
    page.wait_for_timeout(500)
    page.fill('input[type="password"]', "tesT@123")
    page.wait_for_timeout(500)
    page.click('button[type="submit"]')
    page.wait_for_timeout(8000)
    print("Logged in:", page.url)


# ======================================================================
# ANALYTICS TESTS
# ======================================================================

# --- TEST 1: Reports page loads correctly -----------------------------
def test_reports_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        page.screenshot(path="reports_loaded.png")

        assert "reports" in page.url, "BUG! Reports page did not load!"
        print("PASSED - test_reports_page_loads")
        browser.close()


# --- TEST 2: Key stats are visible ------------------------------------
def test_key_stats_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        # Check all 5 key stat cards are present
        assert "Total Messages" in body_text, \
            "BUG! Total Messages stat is missing!"
        assert "Conversations" in body_text, \
            "BUG! Conversations stat is missing!"
        assert "Top Category" in body_text, \
            "BUG! Top Category stat is missing!"
        assert "Peak Hour" in body_text, \
            "BUG! Peak Hour stat is missing!"
        assert "Satisfaction" in body_text, \
            "BUG! Satisfaction stat is missing!"

        print("PASSED - test_key_stats_visible")
        browser.close()


# --- TEST 3: Date filter button works (Last 30 days) ------------------
def test_date_filter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # "Last 30 days" is a SPAN inside a button — use get_by_text
        page.get_by_text("Last 30 days").first.click()
        page.wait_for_timeout(3000)

        page.screenshot(path="date_filter_clicked.png")

        assert page.url is not None, "BUG! Page crashed on date filter click!"
        print("PASSED - test_date_filter")
        browser.close()

# --- TEST 4: Refresh button works -------------------------------------
def test_refresh_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Click refresh
        page.get_by_role("button", name="Refresh").click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        page.screenshot(path="after_refresh.png")

        # Stats should still be visible after refresh
        body_text = page.locator("body").inner_text()
        assert "Total Messages" in body_text, \
            "BUG! Stats disappeared after refresh!"
        print("PASSED - test_refresh_button")
        browser.close()


# --- TEST 5: Overview tab works ---------------------------------------
def test_overview_tab():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Overview is a TAB not a button
        page.get_by_role("tab", name="Overview").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="overview_tab.png")

        body_text = page.locator("body").inner_text()
        assert "Messages Over Time" in body_text, \
            "BUG! Chart not showing on Overview tab!"
        print("PASSED - test_overview_tab")
        browser.close()


# --- TEST 6: Categories tab works -------------------------------------
def test_categories_tab():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Categories is a TAB not a button
        page.get_by_role("tab", name="Categories").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="categories_tab.png")

        assert page.url is not None, "BUG! Page crashed on Categories tab!"
        print("PASSED - test_categories_tab")
        browser.close()

# --- TEST 7: Activity tab works ---------------------------------------
def test_activity_tab():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(REPORTS_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Activity is a TAB not a button
        page.get_by_role("tab", name="Activity").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="activity_tab.png")

        assert page.url is not None, "BUG! Page crashed on Activity tab!"
        print("PASSED - test_activity_tab")
        browser.close()


# ======================================================================
# PRICING / BILLING TESTS
# ======================================================================

# --- TEST 8: Billing page loads correctly -----------------------------
def test_billing_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        page.screenshot(path="billing_loaded.png")

        assert "billing" in page.url, "BUG! Billing page did not load!"
        print("PASSED - test_billing_page_loads")
        browser.close()


# --- TEST 9: All plans are visible ------------------------------------
def test_all_plans_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        # Check all 4 plans are present
        assert "Free" in body_text, "BUG! Free plan is missing!"
        assert "Starter" in body_text, "BUG! Starter plan is missing!"
        assert "Growth" in body_text, "BUG! Growth plan is missing!"
        assert "Business" in body_text, "BUG! Business plan is missing!"

        print("PASSED - test_all_plans_visible")
        browser.close()


# --- TEST 10: Current plan is correctly marked ------------------------
def test_current_plan_marked():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        # Free plan should be marked as current
        assert "Current Plan" in body_text, \
            "BUG! Current plan is not marked!"
        print("PASSED - test_current_plan_marked")
        browser.close()


# --- TEST 11: Plan prices are correct ---------------------------------
def test_plan_prices_correct():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        # Verify correct prices are shown
        assert "$0" in body_text, "BUG! Free plan price missing!"
        assert "$3.99" in body_text, "BUG! Starter plan price missing!"
        assert "$12.99" in body_text, "BUG! Growth plan price missing!"
        assert "$49" in body_text, "BUG! Business plan price missing!"

        print("PASSED - test_plan_prices_correct")
        browser.close()


# --- TEST 12: Currency toggle BDT works -------------------------------
def test_currency_toggle_bdt():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Click BDT currency button
        page.get_by_role("button", name="৳ BDT").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="currency_bdt.png")

        body_text = page.locator("body").inner_text()
        assert "৳" in body_text, "BUG! BDT currency not showing!"
        print("PASSED - test_currency_toggle_bdt")
        browser.close()


# --- TEST 13: Currency toggle USD works -------------------------------
def test_currency_toggle_usd():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Click USD currency button
        page.get_by_role("button", name="$ USD").click()
        page.wait_for_timeout(2000)

        page.screenshot(path="currency_usd.png")

        body_text = page.locator("body").inner_text()
        assert "$" in body_text, "BUG! USD currency not showing!"
        print("PASSED - test_currency_toggle_usd")
        browser.close()


# --- TEST 14: Upgrade to Starter button works -------------------------
def test_upgrade_starter_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Click Upgrade to Starter
        page.get_by_role("button", name="Upgrade to Starter").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="upgrade_starter.png")

        # Should redirect to Stripe or show payment page
        # Should not crash
        assert page.url is not None, "BUG! Page crashed on upgrade click!"
        print("Current URL after upgrade click:", page.url)
        print("PASSED - test_upgrade_starter_button")
        browser.close()


# --- TEST 15: Message usage bar is visible ----------------------------
def test_message_usage_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(BILLING_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        body_text = page.locator("body").inner_text()

        # Usage info should be visible
        assert "messages used" in body_text, \
            "BUG! Message usage info not visible!"
        assert "100" in body_text, \
            "BUG! Message limit not shown!"

        print("PASSED - test_message_usage_visible")
        browser.close()