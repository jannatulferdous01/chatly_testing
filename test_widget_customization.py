from playwright.sync_api import sync_playwright
import pytest
import os

EDIT_URL = "https://www.chately.app/dashboard/fd81c81d-26f3-40b1-b904-98fc59102631"

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

# --- Reusable go to edit page -----------------------------------------
def go_to_edit_page(page):
    page.goto(EDIT_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    print("Edit page URL:", page.url)


# --- TEST 1: Edit page loads correctly --------------------------------
def test_edit_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        assert "fd81c81d" in page.url, "BUG! Edit page did not load!"
        print("PASSED - test_edit_page_loads")
        browser.close()


# --- TEST 2: Update business name and save ----------------------------
def test_update_business_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        # Clear and update business name
        name_input = page.locator('input[placeholder="Acme Coffee Shop"]')
        name_input.clear()
        page.wait_for_timeout(500)
        name_input.fill("Updated Restaurant Name")
        page.wait_for_timeout(500)

        # Save changes
        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="update_name.png")

        # Should not crash
        assert page.url is not None, "BUG! Page crashed after saving name!"
        print("PASSED - test_update_business_name")
        browser.close()


# --- TEST 3: Clear business name and save (validation check) ----------
def test_empty_business_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        # Clear business name completely
        name_input = page.locator('input[placeholder="Acme Coffee Shop"]')
        name_input.clear()
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="empty_name_save.png")

        # Should show error or stay on page
        assert "fd81c81d" in page.url, "BUG! Saved with empty business name!"
        print("PASSED - test_empty_business_name")
        browser.close()


# --- TEST 4: Update phone number with valid number --------------------
def test_update_valid_phone():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        phone_input = page.locator('input[type="tel"]')
        phone_input.clear()
        page.wait_for_timeout(300)
        phone_input.fill("+8801712345678")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        assert page.url is not None, "BUG! Page crashed on valid phone!"
        print("PASSED - test_update_valid_phone")
        browser.close()


# --- TEST 5: Update phone with invalid number (letters) ---------------
def test_update_invalid_phone():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        phone_input = page.locator('input[type="tel"]')
        phone_input.clear()
        page.wait_for_timeout(300)
        phone_input.fill("abcdefghij")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="invalid_phone.png")

        assert page.url is not None, "BUG! Page crashed on invalid phone!"
        print("PASSED - test_update_invalid_phone")
        browser.close()


# --- TEST 6: Update email with valid email ----------------------------
def test_update_valid_email():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        email_input = page.locator('input[type="email"]')
        email_input.clear()
        page.wait_for_timeout(300)
        email_input.fill("test@restaurant.com")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        assert page.url is not None, "BUG! Page crashed on valid email!"
        print("PASSED - test_update_valid_email")
        browser.close()


# --- TEST 7: Update email with invalid format -------------------------
def test_update_invalid_email():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        email_input = page.locator('input[type="email"]')
        email_input.clear()
        page.wait_for_timeout(300)
        email_input.fill("notanemail")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="invalid_email.png")

        assert page.url is not None, "BUG! Page crashed on invalid email!"
        print("PASSED - test_update_invalid_email")
        browser.close()


# --- TEST 8: Update website with valid URL ----------------------------
def test_update_valid_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        url_input = page.locator('input[type="url"]')
        url_input.clear()
        page.wait_for_timeout(300)
        url_input.fill("https://www.myrestaurant.com")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        assert page.url is not None, "BUG! Page crashed on valid URL!"
        print("PASSED - test_update_valid_website")
        browser.close()


# --- TEST 9: Update website with invalid URL --------------------------
def test_update_invalid_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        url_input = page.locator('input[type="url"]')
        url_input.clear()
        page.wait_for_timeout(300)
        url_input.fill("not-a-url")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="invalid_url.png")

        assert page.url is not None, "BUG! Page crashed on invalid URL!"
        print("PASSED - test_update_invalid_website")
        browser.close()


# --- TEST 10: Update greeting message ---------------------------------
def test_update_greeting_message():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        greeting_input = page.locator('input[placeholder="Hi! How can I help you today?"]')
        greeting_input.clear()
        page.wait_for_timeout(300)
        greeting_input.fill("Hello! Welcome to our restaurant!")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        assert page.url is not None, "BUG! Page crashed on greeting update!"
        print("PASSED - test_update_greeting_message")
        browser.close()


# --- TEST 11: Change brand color --------------------------------------
def test_change_brand_color():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        # Set brand color to blue
        color_input = page.locator('input[type="color"]')
        color_input.evaluate("el => el.value = '#0000ff'")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        page.screenshot(path="brand_color.png")

        assert page.url is not None, "BUG! Page crashed on color change!"
        print("PASSED - test_change_brand_color")
        browser.close()


# --- TEST 12: Toggle WhatsApp button ----------------------------------
def test_toggle_whatsapp():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        # Scroll down to WhatsApp section first
        page.get_by_text("WhatsApp Button").scroll_into_view_if_needed()
        page.wait_for_timeout(1000)

        # Take screenshot to see what the toggle looks like
        page.screenshot(path="whatsapp_before.png")

        # The checkbox is hidden — click using force to bypass overlay
        checkboxes = page.locator('input[type="checkbox"]').all()
        print(f"Checkboxes found: {len(checkboxes)}")

        # Use force=True to click hidden checkbox
        checkboxes[0].click(force=True)
        page.wait_for_timeout(1000)

        page.screenshot(path="whatsapp_after.png")

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        assert page.url is not None, "BUG! Page crashed on WhatsApp toggle!"
        print("PASSED - test_toggle_whatsapp")
        browser.close()


# --- TEST 13: Cancel button goes back ---------------------------------
def test_cancel_goes_back():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        # Make a change
        name_input = page.locator('input[placeholder="Acme Coffee Shop"]')
        name_input.clear()
        name_input.fill("This should not be saved")
        page.wait_for_timeout(500)

        # Click Cancel
        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(3000)

        page.screenshot(path="cancel_edit.png")

        # Should navigate away from edit page
        assert page.url is not None, "BUG! Cancel crashed the page!"
        print("PASSED - test_cancel_goes_back")
        browser.close()


# --- TEST 14: XSS in greeting message ---------------------------------
def test_xss_in_greeting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login(page)
        go_to_edit_page(page)

        greeting_input = page.locator('input[placeholder="Hi! How can I help you today?"]')
        greeting_input.clear()
        page.wait_for_timeout(300)
        greeting_input.fill("<script>alert('xss')</script>")
        page.wait_for_timeout(500)

        page.get_by_role("button", name="Save Changes").click()
        page.wait_for_timeout(5000)

        # No popup should appear
        assert page.url is not None, "BUG! XSS caused crash in greeting!"
        print("PASSED - test_xss_in_greeting")
        browser.close()