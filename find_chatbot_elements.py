# find_chatbot_elements.py
from playwright.sync_api import sync_playwright

def find_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Login first
        page.goto("https://www.chately.app/auth/login")
        page.wait_for_load_state("networkidle")
        
        #  Put your login details
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.fill('input[type="password"]', "tesT@123")
        
        #  Put your working submit button selector from Day 1
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle", timeout=15000)
        
        print(" Logged in. Current URL:", page.url)

        # Find the "Create Chatbot" button
        buttons = page.locator("button").all()
        print(f"\nTotal buttons: {len(buttons)}")
        for i, btn in enumerate(buttons):
            print(f"Button {i}: '{btn.inner_text().strip()}'")
        print(" Logged in. Current URL:", page.url)
        # Find all links
        links = page.locator("a").all()
        print(f"\nTotal links: {len(links)}")
        for i, link in enumerate(links):
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if text:
                print(f"Link {i}: '{text}' → {href}")

        browser.close()

find_elements()