## 2025-10-27 - Polling vs DOMContentLoaded
**Learning:** Legacy code often uses `setTimeout` loops (polling) to wait for dependencies like jQuery when scripts are loaded asynchronously. This is a "busy-wait" antipattern that wastes main thread cycles. Modern deferred loading (`<script defer>`) guarantees execution order, making `DOMContentLoaded` the correct and performant synchronization point.
**Action:** When optimizing legacy sites, replace `setTimeout` recursion for dependency checking with `DOMContentLoaded` listeners or Promise-based waits if the dependency supports it.
