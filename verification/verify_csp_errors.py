import threading
import http.server
import socketserver
import time
from playwright.sync_api import sync_playwright

PORT = 8081

def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def verify_csp_errors():
    # Start server in a separate thread
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Wait for server to start

    with sync_playwright() as p:
        # Launch browser - bypass_csp=False is default, but ensuring it.
        # However, checking CSP violations often requires the browser to ENFORCE it.
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(msg))
        page.on("pageerror", lambda err: console_messages.append(f"PAGE ERROR: {err}"))

        print(f"Navigating to http://localhost:{PORT}/index.html")
        page.goto(f"http://localhost:{PORT}/index.html")

        # Wait a bit for any async scripts to load and trigger potential CSP errors
        page.wait_for_timeout(3000)

        # Take a screenshot
        screenshot_path = "verification/csp_verification.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Check for CSP errors in console
        csp_violations = [msg.text for msg in console_messages if "Content Security Policy" in msg.text]

        if csp_violations:
            print("❌ CSP Violations found:")
            for v in csp_violations:
                print(f"  - {v}")
        else:
            print("✅ No CSP Violations found in console.")

        # Also print all console errors for debugging
        errors = [msg.text for msg in console_messages if msg.type == "error"]
        if errors:
            print("⚠️ Other Console Errors:")
            for e in errors:
                print(f"  - {e}")

if __name__ == "__main__":
    verify_csp_errors()
