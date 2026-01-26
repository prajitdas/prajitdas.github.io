## 2025-10-27 - [False Positive Security Tooling]
**Vulnerability:** The vulnerability assessment tool (`vulnerability_assessment.py`) flagged `X-Frame-Options` as missing and marked it as [CRITICAL], even though the site uses a JS frame buster and is hosted on GitHub Pages (static).
**Learning:** `X-Frame-Options` is strictly an HTTP response header and is ignored by browsers if set via a `<meta>` tag. Adding it to HTML is "security theater" and violates Sentinel's principles. Furthermore, automated tools checking for headers via `<meta>` tags (like the one in this repo) can be misleading if not carefully designed to distinguish between what works in headers vs. meta tags.
**Prevention:**
1. Do not use `<meta http-equiv="X-Frame-Options">`.
2. For static sites where headers can't be set, rely on CSP `frame-ancestors` (if supported) or JS frame-busters.
3. Update security tooling to recognize the limitations of the hosting environment (e.g., localhost vs. prod) and to avoid recommending ineffective fixes.

## 2025-10-27 - [CSP Granularity for Analytics]
**Vulnerability:** Google Analytics integration was blocked by the Content Security Policy despite `google-analytics.com` being whitelisted.
**Learning:** `connect-src` must explicitly include `https://stats.g.doubleclick.net` for modern Google Analytics (GA4/Universal) to function correctly, as it offloads some data collection there.
**Prevention:** When implementing strict CSP, verify all third-party dependencies' network activity in the browser console, as they often communicate with undocumented subdomains or affiliated services.
