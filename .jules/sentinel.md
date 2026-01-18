## 2025-10-27 - [False Positive Security Tooling]
**Vulnerability:** The vulnerability assessment tool (`vulnerability_assessment.py`) flagged `X-Frame-Options` as missing and marked it as [CRITICAL], even though the site uses a JS frame buster and is hosted on GitHub Pages (static).
**Learning:** `X-Frame-Options` is strictly an HTTP response header and is ignored by browsers if set via a `<meta>` tag. Adding it to HTML is "security theater" and violates Sentinel's principles. Furthermore, automated tools checking for headers via `<meta>` tags (like the one in this repo) can be misleading if not carefully designed to distinguish between what works in headers vs. meta tags.
**Prevention:**
1. Do not use `<meta http-equiv="X-Frame-Options">`.
2. For static sites where headers can't be set, rely on CSP `frame-ancestors` (if supported) or JS frame-busters.
3. Update security tooling to recognize the limitations of the hosting environment (e.g., localhost vs. prod) and to avoid recommending ineffective fixes.

## 2025-10-27 - [Broken Security Tooling & Reverse Tabnabbing]
**Vulnerability:** The security scanner (`comprehensive_security_scan.py`) was misconfigured to scan only the `.github` directory, missing the entire codebase. This hid reverse tabnabbing vulnerabilities in `assets/js/enhanced-csi.js`.
**Learning:** Security tools are software too and can have bugs. Always verify that your security tools are actually scanning the intended target (check file counts, paths). A "green" build means nothing if the coverage is zero.
**Prevention:**
1. Fix the `base_dir` resolution in scanning scripts to reliably find the repo root.
2. Add regression tests or assertions in security tools to ensure they scanned > 0 files.
3. Use automated checks for `target="_blank"` missing `rel="noopener"`.
