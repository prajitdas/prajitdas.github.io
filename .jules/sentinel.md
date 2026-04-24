# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-02-24 - [Strict Iframe Sandboxing for Third-Party Embeds]
**Vulnerability:** A dynamically generated YouTube iframe in `assets/js/main.js` lacked strict `sandbox` policies. Although the site CSP enforces `frame-src 'self' https://www.youtube.com`, omitting iframe sandbox flags gives the third-party window unnecessary privileges to navigate the top-level browsing context, run unneeded features, and submit forms.
**Learning:** Third-party widgets like YouTube embeds need to be explicitly sandboxed to enforce least privilege. However, when sandboxing YouTube iframes, `allow-same-origin` is required for the player to function correctly (otherwise it breaks video playback). The appropriate set of minimum permissions for a YouTube embed is `allow-scripts allow-popups allow-presentation allow-same-origin`.
**Prevention:** Always apply the `sandbox` attribute to dynamically created or static iframes pointing to third-party domains. Use the principle of least privilege, adding only the sandbox flags required for the embed to function properly.
