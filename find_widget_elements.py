# find_widget_elements.py
from playwright.sync_api import sync_playwright

def find_widget():
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
        print(" Logged in:", page.url)

        # Go to chatbots list
        page.click('a[href="/dashboard"]')
        page.wait_for_timeout(3000)

        # Take screenshot of dashboard
        page.screenshot(path="dashboard_with_chatbot.png")
        print(" Screenshot: dashboard_with_chatbot.png")

        # Print all links — find the chatbot link
        links = page.locator("a").all()
        print(f"\n Links found: {len(links)}")
        for i, link in enumerate(links):
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if text:
                print(f"  Link {i}: '{text}' → {href}")

        # Print all buttons
        buttons = page.locator("button").all()
        print(f"\n Buttons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        browser.close()

find_widget()