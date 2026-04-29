# find_edit_page.py
from playwright.sync_api import sync_playwright

EDIT_URL = "https://www.chately.app/dashboard/fd81c81d-26f3-40b1-b904-98fc59102631"

def find_edit_elements():
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

        # Go to edit page
        page.goto(EDIT_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        print("Edit page URL:", page.url)

        # Take screenshot
        page.screenshot(path="edit_page.png")
        print("Screenshot saved: edit_page.png")

        # Print all inputs
        inputs = page.locator("input").all()
        print(f"\nInputs found: {len(inputs)}")
        for i, inp in enumerate(inputs):
            print(f"  Input {i}: type='{inp.get_attribute('type')}' | "
                  f"placeholder='{inp.get_attribute('placeholder')}' | "
                  f"name='{inp.get_attribute('name')}'")

        # Print all textareas
        textareas = page.locator("textarea").all()
        print(f"\nTextareas found: {len(textareas)}")
        for i, ta in enumerate(textareas):
            print(f"  Textarea {i}: placeholder='{ta.get_attribute('placeholder')}'")

        # Print all buttons
        buttons = page.locator("button").all()
        print(f"\nButtons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        browser.close()

find_edit_elements()