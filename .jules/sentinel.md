# Sentinel's Journal

## 2025-02-24 - [CSP Hardening and Inline Script Consolidation]
**Vulnerability:** The website's Content Security Policy (CSP) allowed `'unsafe-inline'` in `script-src`, leaving it vulnerable to Cross-Site Scripting (XSS). Inline scripts for Analytics, Web Vitals, and Service Worker registration were scattered throughout `index.html`.
**Learning:** Moving non-critical inline scripts to a single external file (`assets/js/security-init.js`) enables a stricter CSP. However, critical scripts like Anti-clickjacking and CSS loading must remain inline for performance and security, requiring their SHA-256 hashes to be explicitly allowed in the CSP. Inline event handlers (like `onload`) also violate strict CSP and must be refactored into external scripts.
**Prevention:** Design new pages with strict CSP in mind. Avoid inline scripts and event handlers. Use Subresource Integrity (SRI) for all external scripts to prevent tampering.

## 2025-02-24 - [Consistent CSP on Error Pages]
**Vulnerability:** The `404.html` page had a weaker Content Security Policy (CSP) allowing `'unsafe-inline'` and lacked the essential security initialization script (`assets/js/security-init.js`) found in `index.html`. This created a potential attack vector if an attacker could lure a user to a non-existent URL.
**Learning:** Security configurations (CSP, SRI, Headers) must be consistent across all pages, including error pages (404, 500). Error pages are often overlooked during security audits but share the same origin and can be exploited.
**Prevention:** Treat `404.html` as a first-class citizen in the security architecture. Ensure it imports the same security-hardened scripts and uses the same strict CSP headers as the main application. Verify error pages during security testing.

## 2025-03-08 - [Hardcoding SRI Hashes on Same-Origin Static Scripts]
**Vulnerability:** Adding Subresource Integrity (SRI) `integrity` attributes with hardcoded SHA hashes to local, same-origin static scripts (e.g., `<script src="assets/js/modern.js" integrity="...">`) in HTML files without an automated build pipeline.
**Learning:** Hardcoding SRI for same-origin scripts introduces severe fragility. Any minor difference (e.g., line endings changing from CRLF to LF during git checkout across OS environments) invalidates the hash. Since LLMs can hallucinate hashes, and static setups lack a build step to dynamically compute them, the browser will permanently block the script, leading to functional regressions.
**Prevention:** Only use SRI for third-party scripts loaded from CDNs where you do not control the remote server. For same-origin files in static deployments, trust the delivery mechanism (HTTPS/GitHub Pages) and omit `integrity` attributes unless there is a robust, automated build pipeline (like Webpack or Rollup) calculating them dynamically.
