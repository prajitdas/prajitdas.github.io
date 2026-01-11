# Sentinel's Journal

## 2025-05-23 - Critical jQuery Vulnerability Fix
**Vulnerability:** jQuery 1.11.2 was being used, which has multiple known XSS vulnerabilities (e.g., CVE-2015-9251, CVE-2020-11022).
**Learning:** Upgrading from 1.x to 3.x requires `jquery-migrate` to be present, and crucially, the service worker cache needs to be invalidated (by version bump) to ensure users get the new files.
**Prevention:** Regularly check `npm audit` or equivalent for frontend libraries, even in static sites.
