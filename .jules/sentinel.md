# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-02-24 - [Remove unsafe-inline from script-src]
**Vulnerability:** Across multiple HTML files (e.g., `modern.html`, `projects.html`, `experience.html`, `publications.html`, `service.html`, `404.html`) and the `.htaccess` configuration, the Content Security Policy (CSP) permitted `'unsafe-inline'` in the `script-src` and `default-src` directives. This misconfiguration could allow an attacker to execute malicious scripts injected into the page, circumventing XSS protections.
**Learning:** It is crucial to maintain strict CSP headers on all pages and configurations, forbidding inline script execution. Functionality reliant on inline JavaScript (like event handlers and email obfuscators) must be moved into external JavaScript files.
**Prevention:** Externalize all JavaScript code into dedicated `.js` files and serve them securely. Ensure CSP headers exclusively list trusted origins and never permit `'unsafe-inline'` for scripts.
