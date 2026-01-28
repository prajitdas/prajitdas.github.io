## 2026-01-27 - Neglected 404 Pages in Static Sites
**Vulnerability:** The `404.html` file referenced a dead dependency (`jquery-migrate`) and lacked the Content Security Policy (CSP) and Subresource Integrity (SRI) controls present in `index.html`.
**Learning:** In static site setups, `404.html` often suffers from "configuration drift," missing security headers and dependency updates applied to the main page. This makes it a potential vector for XSS or component hijacking if it loads dead or insecure scripts.
**Prevention:** Treat `404.html` as a primary entry point in validation pipelines. Ensure security scripts verify headers and integrity hashes on error pages just as strictly as on the home page.
