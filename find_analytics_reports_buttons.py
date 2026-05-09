# find_reports_buttons.py
from playwright.sync_api import sync_playwright

def find_reports():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.chately.app/auth/login")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.wait_for_timeout(500)
        page.fill('input[type="password"]', "tesT@123")
        page.wait_for_timeout(500)
        page.click('button[type="submit"]')
        page.wait_for_timeout(8000)

        page.goto("https://www.chately.app/dashboard/reports")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        page.screenshot(path="reports_detail.png")

        # Print ALL buttons with exact text
        print("--- BUTTONS ---")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        # Print ALL tabs
        print("\n--- TABS ---")
        tabs = page.locator('[role="tab"]').all()
        for i, tab in enumerate(tabs):
            print(f"  Tab {i}: '{tab.inner_text().strip()}'")

        # Print all clickable text elements
        print("\n--- ALL TEXT WITH CLICK ---")
        for tag in ["a", "div", "span", "li"]:
            elements = page.locator(tag).all()
            for el in elements:
                text = el.inner_text().strip()
                if text in ["Last 30 days", "Overview", "Categories",
                            "Activity", "Last 7 days", "Last 90 days"]:
                    tag_name = el.evaluate("el => el.tagName")
                    role = el.get_attribute("role")
                    print(f"  Found: '{text}' | tag={tag_name} | role={role}")

        browser.close()

find_reports()