## 2024-05-23 - Accessibility: Skip to Content
**Learning:** Single-page sites with fixed headers often trap keyboard users in a navigation loop unless a "Skip to Content" link is provided. This is a critical WCAG 2.1 requirement (2.4.1 Bypass Blocks).
**Action:** Always include a visually hidden, focus-visible skip link as the first focusable element in the DOM for pages with repeated navigation headers.

## 2024-05-24 - Accessibility: Visual Indicators
**Learning:** Visual-only indicators (like progress bars or charts) must have accompanying ARIA attributes or off-screen text to be accessible to screen reader users. Without `role="progressbar"` and `aria-label`, a skill bar is just a silent `div`.
**Action:** Always add `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and `aria-label` to custom progress bar components.

## 2025-05-27 - Accessibility: Interactive Media Triggers
**Learning:** Elements that trigger media playback (like custom YouTube thumbnails) must be keyboard-accessible. A clickable `div` is invisible to keyboard users. Using a semantic `<button>` ensures native keyboard support (Enter/Space) and focusability.
**Action:** Replace `div` with `button type="button"` for custom media triggers, ensuring proper `aria-label` and style resets (`border: none`, `appearance: none`).

## 2025-05-27 - UX: Navigation efficiency on long pages
**Learning:** Users often lose context on long, single-page portfolios. A persistent 'Back to Top' button provides a quick escape hatch, improving navigation efficiency without cluttering the sticky header.
**Action:** Implement a floating 'Back to Top' button that appears only after the user has scrolled significantly (e.g., 300px), ensuring it has an `aria-label` for accessibility.

## 2025-05-27 - Accessibility: Tooltips on Icon-Only Buttons
**Learning:** Icon-only buttons (like social links) often lack visible labels, relying on title attributes which aren't always accessible or styled consistently. Adding explicitly initialized tooltips (like Bootstrap's) improves UX for sighted users while 'aria-label' covers screen readers.
**Action:** Always initialize accessible tooltips for icon-only buttons to provide context on hover/focus, and ensure they have a visible focus state.

## 2025-05-27 - Accessibility: Focus Management for Scroll-to-Top
**Learning:** When using JavaScript to scroll the user to the top of the page, simply scrolling is insufficient for keyboard users as their focus remains at the bottom. This creates a disconnect where the visual viewport and keyboard focus are out of sync.
**Action:** Always chain a focus update (e.g., to the navbar brand or a skip link) after the scroll animation completes to restore logical keyboard navigation context.
