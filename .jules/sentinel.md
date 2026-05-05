# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2024-05-18 - Restrict Third-Party Iframe Privileges
**Vulnerability:** Dynamically generated third-party iframes (e.g., YouTube video embeds) were loaded without restricting their privileges using the `sandbox` attribute. This could potentially allow embedded content to execute malicious actions or access sensitive parent window properties.
**Learning:** Even though the iframe source is trusted (YouTube), defense-in-depth principles dictate restricting capabilities to only what is strictly necessary. We need to explicitly allow 'allow-scripts', 'allow-popups', 'allow-presentation', and 'allow-same-origin' for the YouTube player to function, while denying other potentially risky privileges.
**Prevention:** Whenever generating iframes, whether statically in HTML or dynamically via JavaScript, always explicitly include the `sandbox` attribute and follow the principle of least privilege when granting permissions.
