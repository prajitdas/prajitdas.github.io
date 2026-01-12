# Security Policy

## Supported Versions

The following versions of this project are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Main    | :white_check_mark: |

## Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please follow these steps to report it:

1.  **Do not** open a public issue on GitHub.
2.  Email the details of the vulnerability to [prajitdas@umbc.edu](mailto:prajitdas@umbc.edu).
3.  Include as much information as possible, such as:
    *   The type of vulnerability (e.g., XSS, SQL Injection).
    *   Steps to reproduce the issue.
    *   Sample code or a proof of concept.
4.  We will acknowledge your report within 48 hours and provide an estimated timeline for a fix.

## Security Best Practices

This project follows these security principles:
*   **Static Site Security:** Being a static site hosted on GitHub Pages, we rely on GitHub's infrastructure for server-side security.
*   **Content Security Policy (CSP):** We use a strict CSP to mitigate XSS attacks.
*   **Dependency Management:** We regularly update frontend dependencies (jQuery, Bootstrap) to patch known vulnerabilities.
*   **Minimal Attack Surface:** We avoid using database connections or dynamic server-side processing where possible.

Thank you for helping keep this project secure!
