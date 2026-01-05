## 2025-10-26 - Accessibility of Icon-Only Links
**Learning:** The site relies on `title` attributes for icon-only links (social media, navbar toggle). While this provides a tooltip for mouse users, it is inconsistent for screen reader users and does not provide an accessible name in all contexts.
**Action:** Replace or augment `title` attributes with `aria-label` for icon-only interactive elements to ensure robust accessibility.
