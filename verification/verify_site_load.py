import os
from playwright.sync_api import sync_playwright

def verify_site_load():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"Page Error: {exc}"))

        page.goto("http://localhost:8080/index.html")

        # Wait a bit for scripts to execute
        page.wait_for_timeout(2000)

        # Take screenshot
        screenshot_path = os.path.abspath("verification/site_load.png")
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        if errors:
            print("Errors found:")
            for e in errors:
                print(e)
        else:
            print("No console errors found.")

        browser.close()

if __name__ == "__main__":
    verify_site_load()
