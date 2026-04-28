from playwright.sync_api import sync_playwright
import pytest

#  TEST 1: Valid Login
def test_valid_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False means you SEE the browser
        page = browser.new_page()
        
        page.goto("https://www.chately.app/auth/login")
        
        page.fill('input[type="email"]', "softwarear312@gmail.com")
        page.fill('input[type="password"]', "tesT@123")
        page.click('button[type="submit"]')  
        
        # Wait for navigation and check if dashboard appears after login
        page.wait_for_load_state("networkidle", timeout=10000)
        page.wait_for_url("**/dashboard*", timeout=10000)
        assert "dashboard" in page.url
        
        print(" Login test PASSED")
        browser.close()


#  TEST 2: Wrong Password
def test_invalid_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.chately.app/auth/login")
        
        page.fill('input[type="email"]', "spaul212154@bscse.uiu.ac.bd")
        page.fill('input[type="password"]', "WRONG_PASSWORD_123")
        page.click('button[type="submit"]')
        
        # Wait for error message to appear
        page.wait_for_load_state("networkidle", timeout=10000)
        error = page.locator("text=Invalid").first
        error.wait_for(state="visible", timeout=5000)
        assert error.is_visible()
        
        print(" Invalid login test PASSED")
        browser.close()