## 2025-10-27 - [False Positive Security Tooling]
**Vulnerability:** The vulnerability assessment tool (`vulnerability_assessment.py`) flagged `X-Frame-Options` as missing and marked it as [CRITICAL], even though the site uses a JS frame buster and is hosted on GitHub Pages (static).
**Learning:** `X-Frame-Options` is strictly an HTTP response header and is ignored by browsers if set via a `<meta>` tag. Adding it to HTML is "security theater" and violates Sentinel's principles. Furthermore, automated tools checking for headers via `<meta>` tags (like the one in this repo) can be misleading if not carefully designed to distinguish between what works in headers vs. meta tags.
**Prevention:**
1. Do not use `<meta http-equiv="X-Frame-Options">`.
2. For static sites where headers can't be set, rely on CSP `frame-ancestors` (if supported) or JS frame-busters.
3. Update security tooling to recognize the limitations of the hosting environment (e.g., localhost vs. prod) and to avoid recommending ineffective fixes.

## 2026-01-25 - [Bootstrap XSS Vulnerability Upgrade]
**Vulnerability:** The site was using Bootstrap 3.3.4, which has multiple known XSS vulnerabilities (e.g., CVE-2016-10735, CVE-2018-14040).
**Learning:** Upgrading to Bootstrap 3.4.1 (the latest in the 3.x line) is a drop-in replacement that fixes these issues without breaking the layout. Verification of the upgrade required ensuring the SRI hashes in `index.html` matched the new files exactly. Also, local test suites (`run_all_validation.py`) require manual installation of dependencies (`requests`, `beautifulsoup4`, `lxml`) to run successfully in the dev environment.
**Prevention:**
1. Regularly audit frontend dependencies for known CVEs.
2. Use SRI (Subresource Integrity) hashes to ensure the integrity of loaded libraries.
3. Ensure test environments have all necessary dependencies installed to avoid false negatives/positives during validation.
