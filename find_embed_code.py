# find_embed_code.py
from playwright.sync_api import sync_playwright

EMBED_URL = "https://www.chately.app/dashboard/fd81c81d-26f3-40b1-b904-98fc59102631/embed"

def find_embed():
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

        # Go to embed page
        page.goto(EMBED_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        print("Embed page URL:", page.url)

        # Take screenshot
        page.screenshot(path="embed_page.png")
        print("Screenshot saved: embed_page.png")

        # Print all text on page to find embed code
        body_text = page.locator("body").inner_text()
        print("\nPage text:\n", body_text)

        # Print all buttons
        buttons = page.locator("button").all()
        print(f"\nButtons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        # Find code blocks
        codes = page.locator("code, pre").all()
        print(f"\nCode blocks found: {len(codes)}")
        for i, code in enumerate(codes):
            print(f"  Code {i}: '{code.inner_text().strip()[:200]}'")

        browser.close()

find_embed()