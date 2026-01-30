## 2025-10-27 - Polling vs DOMContentLoaded
**Learning:** Legacy code often uses `setTimeout` loops (polling) to wait for dependencies like jQuery when scripts are loaded asynchronously. This is a "busy-wait" antipattern that wastes main thread cycles. Modern deferred loading (`<script defer>`) guarantees execution order, making `DOMContentLoaded` the correct and performant synchronization point.
**Action:** When optimizing legacy sites, replace `setTimeout` recursion for dependency checking with `DOMContentLoaded` listeners or Promise-based waits if the dependency supports it.

## 2025-10-27 - Font Loading Anti-patterns (FOIT vs FOUT)
**Learning:** Found a legacy script manually forcing `visibility: hidden` on `body` to avoid FOUT (Flash of Unstyled Text) while waiting for fonts. This causes FOIT (Flash of Invisible Text), which is strictly worse for perceived performance and FCP (First Contentful Paint).
**Action:** Remove JS-based visibility toggles for fonts. Rely on `font-display: swap` or `optional` in CSS. Content visibility > font correctness.

## 2026-01-17 - Removing jQuery Migrate
**Learning:** Legacy jQuery plugins (like Vegas 1.x) often rely on deprecated methods like `.load()` (for event handling) or `.bind()`. To remove `jquery-migrate` for performance, these plugins must be patched (e.g., replacing `.load(fn)` with `.on('load', fn)`).
**Action:** Inspect plugins for deprecated methods before removing migrate. If source is unavailable, patching the minified/compiled code is a viable strategy if done carefully. Also, verify usage patterns (e.g., `$.plugin` vs `$.fn.plugin`) as legacy code might have incorrect checks that were masked or ignored.

## 2025-10-27 - Write-Only Cache (Dead Code)
**Learning:** Found an inline script in `index.html` that opened a cache (`prajitdas-v2025.11`) and added files to it, but this cache was NEVER read by the Service Worker or any other script. The Service Worker used a completely different cache name.
**Action:** Always verify that caches populated by inline scripts or "fallbacks" are actually consumed by the application. If not, they are just wasting bandwidth and disk space (and main thread time).

## 2025-10-27 - Anti-pattern: Recursive Polling for UI Initialization
**Learning:** Found redundant inline scripts using recursive `setTimeout` to "fix" mobile menu initialization, likely due to past race conditions or broken dependencies. This polling keeps the main thread busy and is fragile.
**Action:** Replace polling with deterministic, robust event handling in the main deferred bundle. Removing conflicting listeners (by replacing the element or unbinding) is often cleaner than trying to coordinate multiple "fixer" scripts.

## 2025-10-27 - Double Download Anti-Pattern
**Learning:** Found a profile image loaded natively via <img>, but then immediately swapped to a Gravatar URL via an inline script. This caused two downloads for the same LCP slot, wasting bandwidth and delaying visual stability.
**Action:** Remove the JavaScript-based swap. Rely on the native <img> tag and Service Worker caching for the critical LCP image. Avoid using JS to determine the source of critical above-the-fold images.

## 2025-01-26 - Scroll Performance & IntersectionObserver
**Learning:** Legacy jQuery code often uses `$(window).scroll()` to toggle visibility of elements like "Back to Top". This fires heavily on the main thread.
**Action:** Replace `window.scroll` listeners with `IntersectionObserver`. Observe a sentinel element (like `.header` or a 1px div at the top). When it leaves the viewport (`!entry.isIntersecting`), show the UI. This offloads the geometry check to the browser's compositor/optimized path.

## 2026-01-30 - Resource Loading: setTimeout vs Preload
**Learning:** Found legacy code using `setTimeout(..., 200)` to inject a CSS link for Google Fonts. This pattern artificially delays resource discovery and fetching, worsening FCP and increasing the risk of FOUT.
**Action:** Replace JS-based injection with standard `<link rel="preload" as="style">` and `<link rel="stylesheet" media="print" onload="this.media='all'">`. This allows the browser's preload scanner to discover the resource immediately while keeping the render path unblocked.
