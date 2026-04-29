# debug_login2.py
from playwright.sync_api import sync_playwright

def debug_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.chately.app/auth/login")
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)  # extra 2 sec wait

        # Check email field is visible before typing
        page.wait_for_selector('input[type="email"]', state="visible")
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.wait_for_timeout(500)  # small pause between fields

        page.wait_for_selector('input[type="password"]', state="visible")
        page.fill('input[type="password"]', "tesT@123")
        page.wait_for_timeout(500)

        # Take screenshot BEFORE clicking — so we can see what page looks like
        page.screenshot(path="before_login.png")
        print(" Screenshot saved: before_login.png")

        page.click('button[type="submit"]')

        # Wait longer after click
        page.wait_for_timeout(8000)

        # Take screenshot AFTER clicking
        page.screenshot(path="after_login.png")
        print(" Screenshot saved: after_login.png")

        print(" Final URL:", page.url)

        browser.close()

debug_login()