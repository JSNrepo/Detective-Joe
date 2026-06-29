
## 2026-06-29 - Optimize Task Polling Loop
**Learning:** In async task polling loops, using full list comprehensions to check for existence causes O(N) memory allocation and processing time per polling cycle, which creates unnecessary overhead in high-frequency checks.
**Action:** Use the `any()` generator expression (e.g., `any(... for ...)`) instead of a list comprehension when checking for condition fulfillment in polling loops to exit early and prevent unnecessary allocations.
