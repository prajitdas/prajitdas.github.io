import os
import threading
import http.server
import socketserver
import time
import re
from playwright.sync_api import sync_playwright, expect

PORT = 8000
SERVER_URL = f"http://localhost:{PORT}"

def run_server():
    # serve from repo root
    Handler = http.server.SimpleHTTPRequestHandler
    # Allow address reuse to prevent "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def verify_back_to_top():
    # Start server in background
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait for server to start
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(bypass_csp=True)

        page.goto(SERVER_URL + "/index.html")

        # Verify initial state: button should exist but NOT have 'visible' class
        button = page.locator("#back-to-top")
        expect(button).to_have_count(1)

        # Check class does not contain 'visible'
        # We can just check the class attribute directly or use expect
        # expect(button).not_to_have_class(re.compile(r"visible"))
        # But wait, class is "back-to-top". "visible" is added.

        print("Initial state: checking if visible class is absent")
        classes = button.get_attribute("class")
        print(f"Initial classes: {classes}")
        if "visible" in classes:
            print("Error: Button has visible class initially")
            exit(1)

        # Scroll down
        print("Scrolling down...")
        page.evaluate("window.scrollTo(0, 1000)")
        # Force a layout/paint frame
        page.wait_for_timeout(1000)

        # Verify button becomes visible
        print("Checking if visible class is present")
        expect(button).to_have_class(re.compile(r"visible"))

        # Take screenshot
        os.makedirs("verification", exist_ok=True)
        page.screenshot(path="verification/back_to_top_visible.png")
        print("Screenshot taken")

        # Scroll back up
        print("Scrolling up...")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        # Verify button becomes hidden (class removed)
        print("Checking if visible class is removed")
        expect(button).not_to_have_class(re.compile(r"visible"))

        browser.close()

if __name__ == "__main__":
    verify_back_to_top()
