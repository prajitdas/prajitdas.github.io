
import os
from playwright.sync_api import sync_playwright, expect

def verify_image():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use bypass_csp=True for file:// access if needed, though mostly relevant for scripts/fetch
        page = browser.new_page(bypass_csp=True)

        file_path = os.path.abspath('index.html')
        page.goto(f"file://{file_path}")

        # Wait for the image to be visible
        img = page.locator("#donottouch")
        expect(img).to_be_visible()

        # Verify src contains 'Profile.jpg'
        src = img.get_attribute("src")
        print(f"Image src: {src}")
        assert "Profile.jpg" in src
        assert "gravatar.com" not in src

        # Verify srcset is NOT set (since we removed the script that sets it)
        # Wait, the script *added* srcset. The static HTML doesn't have it.
        # But let's check just in case.
        srcset = img.get_attribute("srcset")
        if srcset:
            print(f"Image srcset: {srcset}")
            assert "gravatar.com" not in srcset

        page.screenshot(path="verification/profile_image.png")
        browser.close()

if __name__ == "__main__":
    verify_image()
