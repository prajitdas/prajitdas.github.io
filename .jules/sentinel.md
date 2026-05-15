# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-02-24 - [CSP Hardening on Secondary Pages]
**Vulnerability:** The website's secondary pages (`projects.html`, `modern.html`, `404.html`, `experience.html`, `publications.html`, and `service.html`) allowed `'unsafe-inline'` in their Content Security Policy (CSP) `script-src` directive. This was mainly due to inline scripts for UI toggling and email obfuscation, leaving them vulnerable to Cross-Site Scripting (XSS).
**Learning:** Security configurations (CSP) must be consistent and strict across all pages. Refactoring inline scripts into external files (e.g., `assets/js/modern.js`) is a prerequisite for removing `'unsafe-inline'` from `script-src` and strengthening defense in depth. Furthermore, `.htaccess` should enforce this baseline by disallowing `'unsafe-inline'` in `default-src` and restricting it specifically to `style-src` if needed.
**Prevention:** Avoid inline scripts entirely. Always externalize JavaScript into separate files and use strict CSP headers across all HTML files and server configurations. Verify CSP headers and inline script absence during security testing.
