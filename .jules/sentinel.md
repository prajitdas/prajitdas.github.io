# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2026-05-22 - [Refactoring Inline Scripts to Support Strict CSP]
**Vulnerability:** The `modern.html` file contained inline JavaScript for handling UI logic (a "Read More" button and email obfuscation). This practice violates strict Content Security Policy (CSP) best practices by requiring `'unsafe-inline'` in `script-src`, which leaves the site vulnerable to Cross-Site Scripting (XSS).
**Learning:** Even seemingly harmless UI logic must be externalized when aiming for a strict CSP. When extracting inline scripts into external files (e.g., `assets/js/modern.js`), remember to update the Service Worker (`sw.js`) cache lists and bump cache versions to ensure offline functionality and cache invalidation work correctly.
**Prevention:** Avoid inline `<script>` tags entirely when creating new pages or adding functionality. Always place JavaScript logic in external `.js` files and explicitly manage their caching in the Service Worker.

## 2026-06-16 - [CSP Consistency Across HTML Files]
**Vulnerability:** The Content Security Policy (CSP) in the `<meta>` tags of secondary HTML files (like `projects.html`, `publications.html`, `service.html`, `modern.html`, `404.html`, and `experience.html`) incorrectly included `'unsafe-inline'` in their `script-src` directives, violating the strict CSP set in `.htaccess`. Additionally, `index.html` was missing `https://cdnjs.cloudflare.com` from its `script-src`, which caused a mismatch between the `.htaccess` CSP and the HTML `<meta>` CSP.
**Learning:** Browsers enforce the intersection of all active CSPs. If the `.htaccess` file sets a strict CSP but the `<meta>` tags in the HTML files set a different one, the strictest rules from both will apply, potentially breaking legitimate functionality or creating vulnerabilities if they are not perfectly synchronized.
**Prevention:** Ensure that the Content Security Policy (CSP) defined in `.htaccess` exactly matches the CSP defined in the `<meta>` tags of all HTML files. When updating the CSP to remove `'unsafe-inline'`, all instances across the codebase must be updated simultaneously.
