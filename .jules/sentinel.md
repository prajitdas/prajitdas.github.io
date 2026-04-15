# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2026-04-14 - [Third-Party Iframe Sandboxing]
**Vulnerability:** Dynamically injected third-party iframes (e.g., YouTube embeds) in `assets/js/main.js` lacked the `sandbox` attribute, potentially allowing them to execute unwanted actions or escape their isolated context if compromised.
**Learning:** The `sandbox` attribute provides an essential layer of defense-in-depth by restricting the capabilities of embedded content. It's a critical pattern when embedding third-party components that you don't control, preventing them from accessing top-level window objects or executing malicious scripts outside a controlled environment.
**Prevention:** Whenever dynamically or statically creating third-party `iframe` elements, always include the `sandbox` attribute with the least privilege necessary. For YouTube embeds specifically, `allow-same-origin` is required for the player to function properly, so the appropriate configuration is `allow-scripts allow-popups allow-presentation allow-same-origin`.
