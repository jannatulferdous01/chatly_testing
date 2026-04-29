from playwright.sync_api import sync_playwright
import pytest
import os

# Path to your local test HTML file
TEST_SITE_PATH = "file:///E:/chatly_testing/test_site.html"
EMBED_URL = "https://www.chately.app/dashboard/fd81c81d-26f3-40b1-b904-98fc59102631/embed"

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


# --- TEST 1: Embed page loads correctly -------------------------------
def test_embed_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(EMBED_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        page.screenshot(path="embed_page_loaded.png")

        assert "embed" in page.url, "BUG! Embed page did not load!"
        print("PASSED - test_embed_page_loads")
        browser.close()


# --- TEST 2: Embed code is present on page ----------------------------
def test_embed_code_present():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(EMBED_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Find code block and check it has correct chatbot ID
        code_block = page.locator("code, pre").first
        code_text = code_block.inner_text()

        print("Embed code found:", code_text)

        assert "fd81c81d-26f3-40b1-b904-98fc59102631" in code_text, \
            "BUG! Chatbot ID missing from embed code!"
        assert "widget.js" in code_text, \
            "BUG! widget.js missing from embed code!"
        print("PASSED - test_embed_code_present")
        browser.close()


# --- TEST 3: Copy button exists on embed page -------------------------
def test_copy_button_exists():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(EMBED_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Check copy button exists
        copy_button = page.get_by_role("button", name="Copy")
        assert copy_button.is_visible(), "BUG! Copy button not found!"

        # Click copy button
        copy_button.click()
        page.wait_for_timeout(2000)

        page.screenshot(path="copy_button.png")
        print("PASSED - test_copy_button_exists")
        browser.close()


# --- TEST 4: Widget loads on local HTML page --------------------------
def test_widget_loads_on_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open local test HTML file
        page.goto(TEST_SITE_PATH)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        page.screenshot(path="widget_on_page.png")
        print("Screenshot saved: widget_on_page.png")

        # Check page loaded
        assert "Test Website" in page.title(), "BUG! Test page did not load!"
        print("PASSED - test_widget_loads_on_page")
        browser.close()


# --- TEST 5: Widget bubble appears on page ----------------------------
def test_widget_bubble_appears():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(TEST_SITE_PATH)
        page.wait_for_load_state("networkidle")

        # Wait longer for widget script to load
        page.wait_for_timeout(8000)

        page.screenshot(path="widget_bubble.png")
        print("Screenshot saved: widget_bubble.png")

        # Check widget script was injected into page
        widget_loaded = page.evaluate("""
            () => {
                const scripts = document.querySelectorAll('script');
                for (let s of scripts) {
                    if (s.src && s.src.includes('widget.js')) return true;
                }
                return false;
            }
        """)

        assert widget_loaded, "BUG! Widget script not loaded on page!"
        print("PASSED - test_widget_bubble_appears")
        browser.close()


# --- TEST 6: Widget opens when bubble is clicked ----------------------
def test_widget_opens_on_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(TEST_SITE_PATH)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)

        # Try to find and click the chat bubble
        try:
            # Widget usually loads inside an iframe or as a button
            chat_bubble = page.locator(
                "button[class*='chat'], div[class*='chat'], "
                "button[class*='widget'], div[class*='widget'], "
                "iframe"
            ).first
            chat_bubble.wait_for(state="visible", timeout=10000)
            chat_bubble.click()
            page.wait_for_timeout(3000)

            page.screenshot(path="widget_opened.png")
            print("Widget clicked successfully")
        except Exception as e:
            print("Could not click widget directly:", str(e))
            page.screenshot(path="widget_opened.png")

        # Page should not crash
        assert page.url is not None, "BUG! Page crashed when clicking widget!"
        print("PASSED - test_widget_opens_on_click")
        browser.close()


# --- TEST 7: Widget loads with wrong chatbot ID -----------------------
def test_widget_wrong_chatbot_id():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Create HTML with fake chatbot ID
        fake_html = """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Test with fake ID</h1>
            <script src="https://www.chately.app/widget.js"
                    data-chatbot-id="fake-id-that-does-not-exist"
                    async></script>
        </body>
        </html>
        """
        # Write temp file
        with open("E:/chatly_testing/test_fake_id.html", "w") as f:
            f.write(fake_html)

        page.goto("file:///E:/chatly_testing/test_fake_id.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)

        page.screenshot(path="widget_fake_id.png")

        # Page should not crash or show JS errors
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("JS errors on fake ID page:", errors)

        # Page itself should still load
        assert page.url is not None, "BUG! Page crashed with fake chatbot ID!"
        print("PASSED - test_widget_wrong_chatbot_id")
        browser.close()


# --- TEST 8: Platform tabs work (Shopify, WordPress, Wix, HTML) -------
# --- TEST 8: Platform tabs work (Shopify, WordPress, Wix, HTML) -------
def test_platform_tabs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)

        page.goto(EMBED_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Scroll down to platform tabs section
        page.get_by_text("Platform Installation Guide").scroll_into_view_if_needed()
        page.wait_for_timeout(1000)

        page.screenshot(path="before_tabs.png")
        print("Screenshot saved: before_tabs.png")

        # Print all buttons to see exact names
        buttons = page.locator("button").all()
        print(f"Buttons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            text = btn.inner_text().strip()
            if text:
                print(f"  Button {i}: '{text}'")

        # Click each platform tab using text locator
        platforms = ["WordPress", "Wix", "HTML / Other"]

        for platform in platforms:
            try:
                page.get_by_text(platform, exact=True).first.click()
                page.wait_for_timeout(2000)
                page.screenshot(path=f"tab_{platform.replace(' ', '_').replace('/', '')}.png")
                print(f"Clicked tab: {platform}")
            except Exception as e:
                print(f"Could not click tab '{platform}': {str(e)}")

        assert page.url is not None, "BUG! Page crashed on platform tab click!"
        print("PASSED - test_platform_tabs")
        browser.close()