from playwright.sync_api import sync_playwright, expect

def verify_index():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the index.html file locally
        page.goto("file:///app/index.html")

        # Wait for the main heading (H1) to be visible
        # Using .first to be safe, or specificity
        expect(page.locator("h1.name").first).to_be_visible()

        # Wait a bit for animations/scripts
        page.wait_for_timeout(2000)

        # Take a screenshot
        page.screenshot(path="verification/index_screenshot.png", full_page=True)

        print("Verification screenshot taken at verification/index_screenshot.png")

        browser.close()

if __name__ == "__main__":
    verify_index()
