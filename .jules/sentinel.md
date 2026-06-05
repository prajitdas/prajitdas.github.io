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

## 2026-06-05 - [Restrict Third-Party Iframe Privileges]
**Vulnerability:** Dynamically created third-party iframes (e.g., YouTube embeds) in `assets/js/main.js` lacked `sandbox` attributes, potentially exposing the application to Cross-Site Scripting (XSS) and other attacks from the embedded content.
**Learning:** Third-party content embedded via iframes can execute scripts, open popups, and perform other actions that might compromise the host application if not explicitly restricted. When embedding content from external sources (like YouTube), it's crucial to use the `sandbox` attribute to enforce the principle of least privilege. For YouTube, specific permissions like `allow-scripts`, `allow-popups`, `allow-presentation`, and `allow-same-origin` are necessary for the player to function properly while still restricting other potentially harmful capabilities.
**Prevention:** Always include a restrictive `sandbox` attribute when dynamically generating or hardcoding third-party `<iframe>` tags. Only grant the minimum permissions required for the embedded content to function as intended.
