## 2024-05-23 - Accessibility: Skip to Content
**Learning:** Single-page sites with fixed headers often trap keyboard users in a navigation loop unless a "Skip to Content" link is provided. This is a critical WCAG 2.1 requirement (2.4.1 Bypass Blocks).
**Action:** Always include a visually hidden, focus-visible skip link as the first focusable element in the DOM for pages with repeated navigation headers.

## 2024-05-24 - Accessibility: Visual Indicators
**Learning:** Visual-only indicators (like progress bars or charts) must have accompanying ARIA attributes or off-screen text to be accessible to screen reader users. Without `role="progressbar"` and `aria-label`, a skill bar is just a silent `div`.
**Action:** Always add `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and `aria-label` to custom progress bar components.

## 2025-05-27 - Accessibility: Interactive Media Triggers
**Learning:** Elements that trigger media playback (like custom YouTube thumbnails) must be keyboard-accessible. A clickable `div` is invisible to keyboard users. Using a semantic `<button>` ensures native keyboard support (Enter/Space) and focusability.
**Action:** Replace `div` with `button type="button"` for custom media triggers, ensuring proper `aria-label` and style resets (`border: none`, `appearance: none`).
