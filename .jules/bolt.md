## 2025-10-27 - Polling vs DOMContentLoaded
**Learning:** Legacy code often uses `setTimeout` loops (polling) to wait for dependencies like jQuery when scripts are loaded asynchronously. This is a "busy-wait" antipattern that wastes main thread cycles. Modern deferred loading (`<script defer>`) guarantees execution order, making `DOMContentLoaded` the correct and performant synchronization point.
**Action:** When optimizing legacy sites, replace `setTimeout` recursion for dependency checking with `DOMContentLoaded` listeners or Promise-based waits if the dependency supports it.

## 2025-10-27 - Font Loading Anti-patterns (FOIT vs FOUT)
**Learning:** Found a legacy script manually forcing `visibility: hidden` on `body` to avoid FOUT (Flash of Unstyled Text) while waiting for fonts. This causes FOIT (Flash of Invisible Text), which is strictly worse for perceived performance and FCP (First Contentful Paint).
**Action:** Remove JS-based visibility toggles for fonts. Rely on `font-display: swap` or `optional` in CSS. Content visibility > font correctness.

## 2026-01-17 - Removing jQuery Migrate
**Learning:** Legacy jQuery plugins (like Vegas 1.x) often rely on deprecated methods like `.load()` (for event handling) or `.bind()`. To remove `jquery-migrate` for performance, these plugins must be patched (e.g., replacing `.load(fn)` with `.on('load', fn)`).
**Action:** Inspect plugins for deprecated methods before removing migrate. If source is unavailable, patching the minified/compiled code is a viable strategy if done carefully. Also, verify usage patterns (e.g., `$.plugin` vs `$.fn.plugin`) as legacy code might have incorrect checks that were masked or ignored.
