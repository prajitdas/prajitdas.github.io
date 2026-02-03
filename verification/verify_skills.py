import http.server
import socketserver
import threading
import time
from playwright.sync_api import sync_playwright

PORT = 8081

def run_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def verify_skills():
    # Start server in a thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait for server to start
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use bypass_csp=True as per memory instruction for verification scripts
        context = browser.new_context(bypass_csp=True)
        page = context.new_page()

        try:
            print("Navigating to page...")
            page.goto(f"http://localhost:{PORT}/index.html")

            # Wait for content to load
            page.wait_for_load_state("networkidle")

            # Scroll to skills section to trigger IntersectionObserver
            print("Scrolling to skills section...")
            skills_section = page.locator(".skills.aside.section")
            skills_section.scroll_into_view_if_needed()

            # Scroll a bit more to ensure bottom elements are visible
            page.evaluate("window.scrollBy(0, 500)")

            # Wait for animation (transition) to complete or at least start
            # CSS transition is 0.8s
            time.sleep(2.0)

            # Check if inline width is applied
            # The JS should have set style="width: XX%"
            level_bars = page.locator(".level-bar-inner")
            count = level_bars.count()
            print(f"Found {count} level bars.")

            for i in range(count):
                bar = level_bars.nth(i)
                style = bar.get_attribute("style")
                data_level = bar.get_attribute("data-level")
                print(f"Bar {i}: data-level={data_level}, style={style}")

                if not style or "width" not in style:
                    print(f"Error: Bar {i} does not have width style set!")
                    # Try scrolling to it specifically
                    print(f"Scrolling to Bar {i}...")
                    bar.scroll_into_view_if_needed()
                    time.sleep(1)
                    style = bar.get_attribute("style")
                    print(f"Bar {i} after scroll: style={style}")
                    if not style or "width" not in style:
                         print(f"Still no width for Bar {i}")
                         # Continue to verify other bars but mark failure

            # Take screenshot of the skills section
            screenshot_path = "verification/skills_verification.png"
            skills_section.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_skills()
