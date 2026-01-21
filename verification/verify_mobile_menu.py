import os
import time
import re
from playwright.sync_api import sync_playwright, expect

def verify_mobile_menu():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use mobile viewport
        page = browser.new_page(viewport={'width': 375, 'height': 667})

        try:
            # Navigate to the local server
            page.goto("http://localhost:8000")

            # Wait for page load
            page.wait_for_load_state("networkidle")

            # Check for hamburger menu
            # locator('.navbar-toggle')
            toggle_btn = page.locator('.navbar-toggle')
            expect(toggle_btn).to_be_visible()

            print("Toggle button found.")

            # Click it
            toggle_btn.click()

            # Check if menu opens
            # .navbar-collapse should get class 'in'
            # Note: Bootstrap 3 adds 'collapse in' classes.
            navbar_collapse = page.locator('.navbar-collapse')

            # Wait for animation/class change
            # Expect class to contain 'in'
            # We use a regex because other classes are present
            expect(navbar_collapse).to_have_class(re.compile(r'\bin\b'))

            print("Menu opened (class 'in' added).")

            # Take screenshot
            page.screenshot(path="verification/mobile_menu_open.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_mobile_menu()
