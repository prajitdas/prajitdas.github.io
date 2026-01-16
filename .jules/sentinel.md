# Sentinel's Journal

## 2025-05-23 - Critical jQuery Vulnerability Fix
**Vulnerability:** jQuery 1.11.2 was being used, which has multiple known XSS vulnerabilities (e.g., CVE-2015-9251, CVE-2020-11022).
**Learning:** Upgrading from 1.x to 3.x requires `jquery-migrate` to be present, and crucially, the service worker cache needs to be invalidated (by version bump) to ensure users get the new files.
**Prevention:** Regularly check `npm audit` or equivalent for frontend libraries, even in static sites.

## 2026-01-16 - Removal of Vulnerable Legacy Assets
**Vulnerability:** Unused legacy jQuery versions (1.10.0, 1.10.2) were present in the `assets/js` directory. Even if unused, they present a "living off the land" risk if an attacker can reference them.
**Learning:** Static site generators or manual asset management can lead to "asset rot" where old vulnerable files accumulate. Automated scanners or manifest files (like the one in `.github/code/dev-docs/MANIFEST`) are useful for tracking what *should* be there versus what *is* there.
**Prevention:** Periodically audit the `assets/` directory against the actual usage in HTML/JS files. Remove anything not actively used.
