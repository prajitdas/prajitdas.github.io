# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2026-04-28 - [CSP Hardening on Secondary Pages and Server Configuration]
**Vulnerability:** The Content Security Policy (CSP) defined in `.htaccess` and secondary HTML pages (`modern.html`, `experience.html`, `projects.html`, `publications.html`, `service.html`, `404.html`) allowed `'unsafe-inline'` in the `script-src` and/or `default-src` directives. This exposed these pages to Cross-Site Scripting (XSS) vulnerabilities.
**Learning:** Security configurations must be strictly applied across all layers. An externalized script in a main page (like `index.html`) is insufficient if secondary pages or the server configuration (`.htaccess`) still broadly allow `'unsafe-inline'`. Additionally, `modern.html` contained an inline script block, necessitating its extraction into `assets/js/modern.js`.
**Prevention:** Ensure all new HTML pages avoid inline scripts and use the strictest possible CSP. Consistently apply CSP hardening across server configurations (`.htaccess`) and all HTML headers. Always verify that secondary or error pages do not relax the security posture established by the main page.
