import threading
import http.server
import socketserver
import sys
import time
from playwright.sync_api import sync_playwright, expect

PORT = 8000

def start_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def verify_css_loading():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(bypass_csp=True)

        print("Navigating to page...")
        page.goto(f"http://localhost:{PORT}/index.html")

        # Check for loadCSS function in source (should be ABSENT)
        content = page.content()
        if "function loadCSS" not in content:
            print("✅ 'loadCSS' function NOT found in source (Optimization confirmed).")
        else:
            print("❌ 'loadCSS' function found in source (FAILED).")

        # Check for presence of preload links
        preload_count = page.locator("link[rel='preload'][as='style']").count()
        print(f"ℹ️ Found {preload_count} preload links.")
        if preload_count >= 4:
            print("✅ Preload links found.")
        else:
            print("❌ Missing preload links.")

        # Check for presence of async links (media=print onload=...)
        # We check if they exist. By the time we check, onload might have fired and media changed to 'all'.
        # But we can check if there are links that match the pattern in the source or have media='all' now.

        # Actually, let's just check if styles are applied.

        # Check for visibility of secondary content
        try:
            expect(page.locator("html")).to_have_class("content-loaded", timeout=5000)
            print("✅ 'content-loaded' class added to html element.")

            # Check opacity of secondary content
            secondary = page.locator(".secondary").first
            opacity = secondary.evaluate("el => getComputedStyle(el).opacity")
            print(f"ℹ️ Secondary content opacity: {opacity}")
            if float(opacity) > 0:
                 print("✅ Secondary content is visible.")
            else:
                 print("❌ Secondary content is NOT visible.")

        except Exception as e:
            print(f"❌ Failed to verify content loading: {e}")

        # Screenshot
        page.screenshot(path="verification/verification.png")
        print("📸 Screenshot saved to verification/verification.png")

        browser.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    try:
        verify_css_loading()
    finally:
        sys.exit(0)
