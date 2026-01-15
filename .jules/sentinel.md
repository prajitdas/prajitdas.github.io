# Sentinel's Journal

## 2025-05-23 - Critical jQuery Vulnerability Fix
**Vulnerability:** jQuery 1.11.2 was being used, which has multiple known XSS vulnerabilities (e.g., CVE-2015-9251, CVE-2020-11022).
**Learning:** Upgrading from 1.x to 3.x requires `jquery-migrate` to be present, and crucially, the service worker cache needs to be invalidated (by version bump) to ensure users get the new files.
**Prevention:** Regularly check `npm audit` or equivalent for frontend libraries, even in static sites.

## 2025-05-24 - Consolidated Security Scripts Pattern
**Vulnerability:** Scattered inline scripts (Analytics, SW, UI logic) make strict CSP (`script-src 'self'`) impossible and are hard to audit.
**Learning:** Legacy Jekyll themes often rely on inline scripts for "performance" (critical path) or convenience. Moving them requires careful handling of execution order (`defer`, `DOMContentLoaded`) and dependencies (jQuery).
**Prevention:** Use a centralized `assets/js/security-scripts.js` for all non-critical, third-party, and security-related logic. Keep only truly critical Frame Busters inline.
