# diagnosis.py
from playwright.sync_api import sync_playwright

def diagnose():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.chately.app/auth/login")
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.fill('input[type="password"]', "tesT@123")
        page.click("text=Sign in")

        # Wait 5 seconds and print where we ended up
        page.wait_for_timeout(5000)
        print("✅ After login URL is:", page.url)

        browser.close()

def diagnose_invalid():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.chately.app/auth/login")
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.fill('input[type="password"]', "WRONG_PASSWORD")
        page.click("text=Sign in")

        # Wait 5 seconds and print error message text
        page.wait_for_timeout(5000)
        print("❌ Page URL after failed login:", page.url)

        # Print ALL visible text on page to find error message
        all_text = page.locator("body").inner_text()
        print("📄 Page text:\n", all_text[:500])  # first 500 chars

        browser.close()

diagnose()
diagnose_invalid()