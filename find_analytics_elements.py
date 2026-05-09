# find_analytics_elements.py
from playwright.sync_api import sync_playwright

def find_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login
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

        # ── REPORTS PAGE ──────────────────────────────────────────────
        print("\n" + "="*50)
        print("REPORTS PAGE")
        print("="*50)
        page.goto("https://www.chately.app/dashboard/reports")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        page.screenshot(path="reports_page.png")
        print("Screenshot saved: reports_page.png")

        buttons = page.locator("button").all()
        print(f"Buttons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        body_text = page.locator("body").inner_text()
        print("\nPage text (first 500 chars):")
        print(body_text[:500])

        # ── BILLING PAGE ──────────────────────────────────────────────
        print("\n" + "="*50)
        print("BILLING PAGE")
        print("="*50)
        page.goto("https://www.chately.app/dashboard/billing")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        page.screenshot(path="billing_page.png")
        print("Screenshot saved: billing_page.png")

        buttons = page.locator("button").all()
        print(f"Buttons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        body_text = page.locator("body").inner_text()
        print("\nPage text (first 800 chars):")
        print(body_text[:800])

        browser.close()

find_all()