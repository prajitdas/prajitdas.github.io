
import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load local file
        file_path = os.path.abspath("index.html")
        page.goto(f"file://{file_path}")

        # Set viewport to mobile
        page.set_viewport_size({"width": 375, "height": 667})

        # Wait for content
        page.wait_for_selector(".navbar-toggle")

        # Take initial screenshot
        page.screenshot(path="verification/mobile_menu_closed.png")
        print("Screenshot taken: closed")

        # Click the toggle button
        page.click(".navbar-toggle")

        # Wait for menu to expand (animation)
        time.sleep(1)

        # Verify class 'in' is present
        # The logic we added: $navbarCollapse.addClass('in'); $navbarCollapse.css('display', 'block');

        collapse_element = page.locator(".navbar-collapse")
        classes = collapse_element.get_attribute("class")
        print(f"Classes after click: {classes}")

        if "in" in classes.split():
            print("SUCCESS: 'in' class added")
        else:
            print("FAILURE: 'in' class NOT added")

        # Take screenshot
        page.screenshot(path="verification/mobile_menu_open.png")
        print("Screenshot taken: open")

        browser.close()

if __name__ == "__main__":
    run()
