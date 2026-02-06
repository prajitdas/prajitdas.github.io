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

## 2026-01-20 - Accessibility: Focus Management with jQuery Animations
**Learning:** When using jQuery animations (like `animate`) to hide or move elements that had focus, standard focus calls might execute before the animation completes or the element is removed.
**Action:** Chain `.promise().then()` to the animation to reliably execute focus management logic (e.g., shifting focus to a container) after the animation queue is fully drained.

## 2026-01-21 - Accessibility: Descriptive Link Text
**Learning:** Vague link text like "here", "read more", or "click here" forces screen reader users to backtrack for context (WCAG 2.4.4). It also creates small, hard-to-hit click targets on touch devices.
**Action:** Always refactor sentences so the link text itself describes the destination (e.g., "Read the [paper from IEEE CIC 2016]" instead of "Read the paper [here]").

## 2026-01-27 - Accessibility: Skip Link Target Focus
**Learning:** A "Skip to main content" link that targets a non-interactive element (like a `div`) will scroll the page but fail to move keyboard focus unless the target has `tabindex="-1"`. This leaves keyboard users stranded at the top of the page.
**Action:** Always add `tabindex="-1"` and `style="outline:none"` to the target container of a skip link to ensure it receives programmatic focus without a visual focus ring.

## 2026-01-30 - Accessibility: Mobile Menu State
**Learning:** Collapsible mobile menus (common in Bootstrap) often toggle visibility visually but fail to communicate state changes to screen readers. The toggle button needs explicit `aria-expanded` updates to inform users if the menu is open or closed.
**Action:** When implementing custom or framework-based collapsible menus, always pair the toggle logic with a state check that updates `aria-expanded="true/false"` on the control button.

## 2026-02-04 - UX: Print Stylesheets as Invisible Accessibility
**Learning:** Users often print portfolio sites to PDF for offline review or archival. Standard web layouts (dark mode, sticky navs) break this experience. Adding a simple print stylesheet is a high-value, low-effort "invisible" feature that respects the user's intent to consume content offline.
**Action:** Always verify pages with `Emulate media print` in devtools or Playwright, ensuring navigation is hidden, contrast is high (black on white), and links are expanded for readability.

## 2026-05-21 - Accessibility: Consistent Focus Visibility
**Learning:** Browser default focus rings are often inconsistent or invisible on custom backgrounds (especially dark ones), causing keyboard users to lose their place. A global `:focus-visible` outline ensures a consistent experience, but high-contrast overrides are necessary for dark sections (like footers).
**Action:** Define a global, high-contrast `:focus-visible` style (e.g., `outline: 3px solid #333`) and specifically override the outline color (e.g., `outline-color: #fff`) for dark containers to ensure WCAG 2.4.7 compliance everywhere.

## 2025-05-28 - UX: Deep Linking for Portfolio Sections
**Learning:** Users often want to share specific parts of a single-page portfolio (e.g., "Check out my experience"). Without IDs on sections and visible permalinks, this is difficult.
**Action:** Add descriptive IDs to all major sections and inject accessible permalinks (anchors) into section headings via JavaScript to enable deep linking without cluttering the initial UI.
