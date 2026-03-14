# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-03-14 - [Complete Removal of Unsafe-Inline from Script-Src]
**Vulnerability:** The website's Content Security Policy (CSP) continued to allow `'unsafe-inline'` in `script-src` and `default-src` to support lingering inline scripts on index.html containing "Read More" and "Email obfuscation" logic. This maintained a significant vulnerability to Cross-Site Scripting (XSS) attacks across the entire application.
**Learning:** To fully harden a web application's CSP, ALL inline scripts must be identified and removed or replaced with external scripts. By extracting the remaining inline logic into a new `assets/js/home.js` file, we were able to successfully drop the `'unsafe-inline'` directive from `script-src` and `default-src` across all HTML pages and server configuration (`.htaccess`).
**Prevention:** Always strive for a strict CSP without `'unsafe-inline'` for scripts. When adding new logic, build it into an external JavaScript file instead of embedding it directly in the HTML file.
