## 2026-01-27 - Neglected 404 Pages in Static Sites
**Vulnerability:** The `404.html` file referenced a dead dependency (`jquery-migrate`) and lacked the Content Security Policy (CSP) and Subresource Integrity (SRI) controls present in `index.html`.
**Learning:** In static site setups, `404.html` often suffers from "configuration drift," missing security headers and dependency updates applied to the main page. This makes it a potential vector for XSS or component hijacking if it loads dead or insecure scripts.
**Prevention:** Treat `404.html` as a primary entry point in validation pipelines. Ensure security scripts verify headers and integrity hashes on error pages just as strictly as on the home page.

## 2026-01-31 - Service Worker Asset Versioning Desynchronization
**Vulnerability:** The Service Worker (`sw.js`) hardcodes asset versions (e.g., `?v=2025.11`) in `STATIC_ASSETS`, which were desynchronized from the actual versions in `index.html` (e.g., `?v=2025.12`). This can lead to the Service Worker caching and serving stale, potentially vulnerable JavaScript files indefinitely, bypassing security patches deployed to the main site.
**Learning:** Manual synchronization of asset versions between HTML and Service Worker files in static sites is error-prone. "Cache-first" strategies can weaponize this by permanently serving outdated code.
**Prevention:** Implement a build step or pre-commit hook that parses `index.html` for asset versions and automatically updates `sw.js` (or vice versa) to ensure the Service Worker always caches the currently deployed assets.
