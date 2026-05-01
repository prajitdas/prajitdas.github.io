# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2026-05-01 - [Sandbox Dynamically Created Iframes]
**Vulnerability:** Dynamically created iframes (like YouTube embeds) in `assets/js/main.js` did not have a `sandbox` attribute. This could allow malicious third-party content or XSS payloads to execute scripts or perform unauthorized actions in the context of the embedding page if the source URL is ever compromised or manipulated.
**Learning:** Even when inserting trusted third-party content, it is crucial to employ the principle of least privilege. The `sandbox` attribute restricts the capabilities of the iframe to the absolute minimum required for functionality (e.g., `allow-scripts allow-popups allow-presentation allow-same-origin` for YouTube embeds).
**Prevention:** Always apply the `sandbox` attribute with the most restrictive set of permissions possible when creating iframes dynamically or statically, especially for content not hosted on the same origin.
