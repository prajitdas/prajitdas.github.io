import sys
from bs4 import BeautifulSoup

def verify_404_security():
    try:
        with open('404.html', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: 404.html not found.")
        sys.exit(1)

    soup = BeautifulSoup(content, 'html.parser')

    # 1. Check for Anti-Clickjacking script
    scripts = soup.find_all('script')
    anti_clickjack_found = False
    for script in scripts:
        if script.string and 'antiClickjack' in script.string and 'self === top' in script.string:
            anti_clickjack_found = True
            break

    if not anti_clickjack_found:
        print("FAIL: Anti-Clickjacking script missing in 404.html")
    else:
        print("PASS: Anti-Clickjacking script found.")

    # 2. Check CSP
    meta_csp = soup.find('meta', {'http-equiv': 'Content-Security-Policy'})
    if not meta_csp:
        print("FAIL: CSP meta tag missing in 404.html")
        sys.exit(1)

    csp_content = meta_csp.get('content', '')

    # Check for Gravatar (should be removed)
    if 'gravatar.com' in csp_content:
        print("FAIL: Gravatar found in CSP (should be removed).")
    else:
        print("PASS: Gravatar not found in CSP.")

    # Check for loadCSS hash (should be removed)
    loadcss_hash = 'sha256-P/tYj7pG4Cv2NnMCcvFFuOLm2uO//ZqTcjbj0S6LefA='
    if loadcss_hash in csp_content:
        print("FAIL: loadCSS hash found in CSP (should be removed).")
    else:
        print("PASS: loadCSS hash not found in CSP.")

    # Check for Anti-Clickjacking hash (should be present)
    ac_hash = 'sha256-EXDMElPmHkgQ0zK8NIkNl5lxOfeOhGKsFbB0TZRxAIQ='
    if ac_hash not in csp_content:
        print("FAIL: Anti-Clickjacking hash missing in CSP.")
    else:
        print("PASS: Anti-Clickjacking hash found in CSP.")

    if anti_clickjack_found and 'gravatar.com' not in csp_content and loadcss_hash not in csp_content and ac_hash in csp_content:
        print("SUCCESS: 404.html security verification passed.")
        sys.exit(0)
    else:
        print("FAILURE: 404.html security verification failed.")
        sys.exit(1)

if __name__ == "__main__":
    verify_404_security()
