## 2026-02-01 - [Securing Generated Artifacts]
**Vulnerability:** Generated HTML files (`my-publications.html`) from `bibtex2html` lacked security headers (CSP) and used insecure HTTP links, bypassing the site's overall security posture.
**Learning:** Build artifacts often escape source-level security checks. Modifying the generation pipeline (`genPubHTML.sh`) to include a post-processing security step (Python script) is more robust than manual fixes. Also, cross-platform compatibility (Linux vs Mac `sed`) in build scripts is a common friction point.
**Prevention:** Always audit generated files. Implement automated post-processing hooks to inject security headers and upgrade links in legacy-generated content.

## 2026-02-02 - [CSP Strictness via Hash-Based Allowlisting]
**Vulnerability:** The site relied on 'unsafe-inline' for script-src in CSP due to scattered inline scripts (Service Worker, Analytics, etc.), effectively weakening XSS protection.
**Learning:** Consolidating non-critical inline scripts into an external file (security-init.js) allowed removing 'unsafe-inline'. For critical inline scripts (anti-clickjacking, critical CSS loader), SHA-256 hashes in the CSP header provide a secure allowlist mechanism without performance penalty.
**Prevention:** Avoid inline scripts where possible. If critical for performance/security, use CSP hashes instead of 'unsafe-inline'.
