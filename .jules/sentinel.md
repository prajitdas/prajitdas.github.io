# Sentinel's Journal

## 2025-05-23 - Critical jQuery Vulnerability Fix
**Vulnerability:** jQuery 1.11.2 was being used, which has multiple known XSS vulnerabilities (e.g., CVE-2015-9251, CVE-2020-11022).
**Learning:** Upgrading from 1.x to 3.x requires `jquery-migrate` to be present, and crucially, the service worker cache needs to be invalidated (by version bump) to ensure users get the new files.
**Prevention:** Regularly check `npm audit` or equivalent for frontend libraries, even in static sites.

## 2025-05-24 - Inline JavaScript Refactor
**Vulnerability:** Excessive use of inline JavaScript in `index.html` (17 occurrences) necessitates the `unsafe-inline` directive in CSP, significantly increasing the attack surface for XSS.
**Learning:** Moving scripts to an external file (`security-scripts.js`) on a static site requires careful handling of execution order (defer), dependency management (jQuery), and ensuring that variables previously in global scope (like `loadYouTubeVideo`) remain accessible if called by inline HTML event handlers.
**Prevention:** Start projects with a strict CSP (`script-src 'self'`) and keep all logic in external files from day one. When refactoring, consolidate scripts into logical units (e.g., security, analytics, UI) and use `defer` to manage dependencies.
