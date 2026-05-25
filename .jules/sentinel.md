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

## 2026-05-25 - [CSP Hardening on Secondary Files and .htaccess]
**Vulnerability:** The `Content-Security-Policy` header in `.htaccess` and the `<meta>` tags in secondary HTML files (e.g., `projects.html`, `publications.html`) allowed `'unsafe-inline'` within their `script-src` and `default-src` directives. This left the application vulnerable to Cross-Site Scripting (XSS) via injected inline scripts on these pages.
**Learning:** CSP must be consistently locked down across all delivery methods (HTTP headers via `.htaccess` and HTML `<meta>` tags). When removing `'unsafe-inline'` from `default-src`, `style-src` may need to be explicitly configured to retain `'unsafe-inline'` if the application still depends on inline styling, preventing unintended breakage while securing script execution.
**Prevention:** Regularly audit CSP declarations in both server configuration files and HTML headers to ensure `'unsafe-inline'` is excluded from `script-src` and `default-src`. Use separated directives (e.g., explicitly separating `style-src` from `script-src` constraints) to manage security policies granularly without breaking presentation logic.
