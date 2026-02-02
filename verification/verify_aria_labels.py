import time
import threading
import http.server
import socketserver
import os
from playwright.sync_api import sync_playwright, expect

PORT = 8082 # Use a different port
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    os.chdir('/app')
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"serving at port {PORT}")
        httpd.serve_forever()

def verify(page):
    page.goto(f"http://localhost:{PORT}/index.html")
    page.wait_for_load_state("networkidle")

    # Check Google Scholar link
    # Bootstrap tooltip removes 'title', so use href
    scholar_link = page.locator('a[href*="scholar.google.com"]')
    expect(scholar_link).to_have_attribute("aria-label", "Google Scholar Profile (opens in a new tab)")
    print("✅ Google Scholar link has correct aria-label")

    # Check GitHub link
    github_link = page.locator('a[href*="github.com/prajitdas"]').first
    expect(github_link).to_have_attribute("aria-label", "GitHub Profile (opens in a new tab)")
    print("✅ GitHub link has correct aria-label")

    # Check a generic link (Cisco)
    cisco_link = page.locator('a[href="https://www.cisco.com"]').first
    sr_only = cisco_link.locator('.sr-only')
    expect(sr_only).to_contain_text("(opens in a new tab)")
    print("✅ Cisco link has .sr-only span")

    # Take screenshot
    header = page.locator('.header').first
    header.screenshot(path="verification/aria_verification.png")

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify(page)
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            exit(1)
        finally:
            browser.close()
