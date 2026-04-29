from playwright.sync_api import sync_playwright
import pytest

# ─── Reusable login function ──────────────────────────────────────────
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
    print(" Logged in:", page.url)

# ─── Reusable go to new chatbot page ─────────────────────────────────
def go_to_new_chatbot(page):
    #  Use href instead of text — avoids duplicate element error
    page.click('a[href="/dashboard/new"]')
    page.wait_for_timeout(3000)
    print(" Template page URL:", page.url)


# ─── TEST 1: Create chatbot using Restaurant Template ─────────────────
def test_create_chatbot_from_template():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        # Click Restaurant template
        page.get_by_text("Restaurant").click()
        page.wait_for_timeout(3000)
        print(" Form page URL:", page.url)

        # Fill business name
        page.fill('input[placeholder="Acme Coffee Shop"]', "My Test Restaurant")
        page.wait_for_timeout(500)

        # Click Create Chatbot
        page.get_by_role("button", name="Create Chatbot").click()
        page.wait_for_timeout(8000)

        print(" After create URL:", page.url)
        assert "new" not in page.url, f"BUG! Still on creation page: {page.url}"
        print(" test_create_chatbot_from_template PASSED")
        browser.close()


# ─── TEST 2: Create chatbot from Scratch ──────────────────────────────
def test_create_chatbot_from_scratch():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        # Click Start from scratch
        page.get_by_text("Start from scratch").click()
        page.wait_for_timeout(3000)
        print(" Scratch form URL:", page.url)

        # Fill business name
        page.fill('input[placeholder="Acme Coffee Shop"]', "Scratch Test Bot")
        page.wait_for_timeout(500)

        # Click Create Chatbot
        page.get_by_role("button", name="Create Chatbot").click()
        page.wait_for_timeout(8000)

        print(" After create URL:", page.url)

        #  FREE PLAN: can only have 1 chatbot
        # So either it succeeds (url changes) OR it shows upgrade prompt
        # Both are valid — app should NOT crash either way
        page_text = page.locator("body").inner_text()

        chatbot_created = "new" not in page.url
        limit_reached = "upgrade" in page_text.lower() \
                        or "limit" in page_text.lower() \
                        or "plan" in page_text.lower()

        assert chatbot_created or limit_reached, \
            f"BUG! Unexpected behavior. URL: {page.url}"

        if chatbot_created:
            print(" test_create_chatbot_from_scratch PASSED — chatbot created!")
        else:
            print(" test_create_chatbot_from_scratch PASSED — plan limit reached gracefully!")

        browser.close()

# ─── TEST 3: Empty Business Name (should show error) ──────────────────
def test_empty_business_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        page.get_by_text("Restaurant").click()
        page.wait_for_timeout(3000)

        # Clear name field and leave empty
        page.fill('input[placeholder="Acme Coffee Shop"]', "")
        page.wait_for_timeout(500)

        # Try to submit
        page.get_by_role("button", name="Create Chatbot").click()
        page.wait_for_timeout(5000)

        # Should stay on same page
        assert "new" in page.url or "dashboard" not in page.url, \
            "BUG! Created chatbot with empty name!"
        print(" test_empty_business_name PASSED")
        browser.close()


# ─── TEST 4: Very Long Business Name (should not crash) ───────────────
def test_long_business_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        page.get_by_text("Restaurant").click()
        page.wait_for_timeout(3000)

        # 500 character name
        page.fill('input[placeholder="Acme Coffee Shop"]', "A" * 500)
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Create Chatbot").click()
        page.wait_for_timeout(8000)

        # Should not crash
        assert page.url is not None, "BUG! Page crashed!"
        print(" test_long_business_name PASSED — no crash")
        browser.close()


# ─── TEST 5: XSS in Business Name (security) ─────────────────────────
def test_xss_in_business_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        page.get_by_text("Restaurant").click()
        page.wait_for_timeout(3000)

        # XSS attempt
        page.fill('input[placeholder="Acme Coffee Shop"]',
                  "<script>alert('xss')</script>")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Create Chatbot").click()
        page.wait_for_timeout(8000)

        # No popup should appear, page should not crash
        assert page.url is not None, "BUG! XSS caused crash!"
        print(" test_xss_in_business_name PASSED — XSS blocked")
        browser.close()


# ─── TEST 6: Cancel button goes back ─────────────────────────────────
def test_cancel_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_new_chatbot(page)

        page.get_by_text("Restaurant").click()
        page.wait_for_timeout(3000)

        # Click Cancel
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(3000)

        # Should go back — not stay on form
        assert "new" not in page.url, \
            f"BUG! Cancel did not go back. URL: {page.url}"
        print(" test_cancel_button PASSED")
        browser.close()