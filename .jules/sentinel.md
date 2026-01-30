## 2025-10-27 - [False Positive Security Tooling]
**Vulnerability:** The vulnerability assessment tool (`vulnerability_assessment.py`) flagged `X-Frame-Options` as missing and marked it as [CRITICAL], even though the site uses a JS frame buster and is hosted on GitHub Pages (static).
**Learning:** `X-Frame-Options` is strictly an HTTP response header and is ignored by browsers if set via a `<meta>` tag. Adding it to HTML is "security theater" and violates Sentinel's principles. Furthermore, automated tools checking for headers via `<meta>` tags (like the one in this repo) can be misleading if not carefully designed to distinguish between what works in headers vs. meta tags.
**Prevention:**
1. Do not use `<meta http-equiv="X-Frame-Options">`.
2. For static sites where headers can't be set, rely on CSP `frame-ancestors` (if supported) or JS frame-busters.
3. Update security tooling to recognize the limitations of the hosting environment (e.g., localhost vs. prod) and to avoid recommending ineffective fixes.

## 2025-10-27 - [Legacy Asset Duplication Risk]
**Vulnerability:** Vulnerable versions of libraries (Bootstrap 3.3.4) were found in `assets/plugins/` even though the site was using upgraded versions in `assets/css/` and `assets/js/`.
**Learning:** The project has a hybrid asset structure where some plugins are in `assets/plugins/` (e.g., Vegas) and others were moved to root `assets/` (Bootstrap, FontAwesome). This inconsistency led to the retention of vulnerable dead code in `assets/plugins/`.
**Prevention:** When refactoring asset locations, ensure the old locations are deleted or strictly documented as "do not use". Verify usage before assuming a directory is safe to delete or safe to keep.
