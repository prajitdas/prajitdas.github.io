## 2024-03-24 - Malformed HTML Security Attributes
**Vulnerability:** Detected several instances of malformed HTML attributes like `target="_blank rel=" noopener""` and `href=url` without quotes.
**Learning:** Copy-pasting HTML code without validation can lead to nested quotes and malformed attributes, which browsers may misinterpret. This can negate security features like `rel="noopener"`, leaving the site vulnerable to reverse tabnabbing.
**Prevention:** Always validate HTML syntax when adding security attributes. Use linters or manual inspection to ensure attributes are correctly quoted and separated.
