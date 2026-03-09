# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-02-24 - [Complete Removal of 'unsafe-inline' from script-src]
**Vulnerability:** The website's Content Security Policy (CSP) headers across `.html` files still allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to XSS. `index.html` contained an inline script handling UI interactions.
**Learning:** The previous consolidation of inline scripts into `assets/js/security-init.js` missed the final inline block in `index.html` (for "Read More" and "Email"). To fully remove `'unsafe-inline'` from `script-src` and `default-src` across the site (including `.htaccess`), all logic had to be moved to an external script (`assets/js/home.js`). We specifically retained `'unsafe-inline'` in `style-src` only, per project requirements.
**Prevention:** Continuously audit CSP headers in both HTML files and `.htaccess` when adding new features. Ensure any new logic is written in external JS files to maintain strict `script-src` boundaries.
