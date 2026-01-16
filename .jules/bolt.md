## 2025-10-27 - Polling vs DOMContentLoaded
**Learning:** Legacy code often uses `setTimeout` loops (polling) to wait for dependencies like jQuery when scripts are loaded asynchronously. This is a "busy-wait" antipattern that wastes main thread cycles. Modern deferred loading (`<script defer>`) guarantees execution order, making `DOMContentLoaded` the correct and performant synchronization point.
**Action:** When optimizing legacy sites, replace `setTimeout` recursion for dependency checking with `DOMContentLoaded` listeners or Promise-based waits if the dependency supports it.

## 2025-10-27 - Font Loading Anti-patterns (FOIT vs FOUT)
**Learning:** Found a legacy script manually forcing `visibility: hidden` on `body` to avoid FOUT (Flash of Unstyled Text) while waiting for fonts. This causes FOIT (Flash of Invisible Text), which is strictly worse for perceived performance and FCP (First Contentful Paint).
**Action:** Remove JS-based visibility toggles for fonts. Rely on `font-display: swap` or `optional` in CSS. Content visibility > font correctness.

## 2025-01-16 - Artificial Delays for Resource Loading
**Learning:** Legacy optimization attempts often use `setTimeout` to "defer" resources like fonts or CSS. This introduces an arbitrary, fixed delay (e.g., 200ms) that penalizes users on fast networks and guarantees a delay even when the browser is idle.
**Action:** Replace JavaScript-based `setTimeout` resource injection with native browser primitives like `<link rel="preload">` and `<link rel="stylesheet" media="print" onload="this.media='all'">` for non-blocking loading without artificial waits.
