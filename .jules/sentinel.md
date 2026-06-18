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

## 2026-06-18 - [Stricter default-src and script-src CSP configuration]
**Vulnerability:** The `.htaccess` file incorrectly had `'unsafe-inline'` set in its `default-src` directive, weakening the overall Content Security Policy (CSP) for all resources on the server. Additionally, multiple secondary HTML files (like `404.html`, `projects.html`) included `'unsafe-inline'` in their `script-src` `<meta>` tags despite not having inline scripts.
**Learning:** `default-src` acts as a fallback for other fetch directives, so including `'unsafe-inline'` there inadvertently weakens the policy for all resource types. Setting strict parameters requires explicit removal of `'unsafe-inline'` and definition of explicitly allowed sources (e.g., specific SHA-256 hashes and domains) for `script-src` and `style-src` in both server-side `.htaccess` configurations and individual HTML `<meta>` tags.
**Prevention:** Avoid defining `'unsafe-inline'` in `default-src`. When adding new HTML pages, default to a strict `script-src` configuration without `'unsafe-inline'` unless explicitly necessary (and preferably use hashes or nonces in those cases). Ensure server-level and HTML-level CSPs are kept synchronized and strict.
