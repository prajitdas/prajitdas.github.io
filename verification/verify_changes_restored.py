
from playwright.sync_api import sync_playwright

def verify_page(page):
    page.goto("http://localhost:8000")

    # Check for console errors
    page.on("console", lambda msg: print(f"Console log: {msg.text}"))
    page.on("pageerror", lambda err: print(f"Page error: {err}"))

    # Wait for body to be visible
    page.wait_for_selector("body")

    # Check if Vegas is loaded (we expect it to be loaded now)
    try:
        page.wait_for_selector(".vegas-background", timeout=5000)
        print("SUCCESS: Vegas background found.")
    except:
        print("FAIL: Vegas background not found!")

    # Check that octicons are NOT requested (we can't easily check network here without more setup,
    # but we can check if the link tag is gone)
    octicon_link = page.query_selector("link[href*='octicons.min.css']")
    if octicon_link:
        print("FAIL: Octicons CSS link found!")
    else:
        print("SUCCESS: Octicons CSS link not found.")

    # Take screenshot
    page.screenshot(path="verification/homepage_restored.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        verify_page(page)
        browser.close()
