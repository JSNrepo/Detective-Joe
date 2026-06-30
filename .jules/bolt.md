## 2026-06-30 - Avoid O(N) allocations in worker polling
**Learning:** Checking pending task status inside a hot while-loop using list comprehensions (`[task for task in tasks if condition]`) creates unnecessary O(N) memory allocations per polling cycle, creating garbage collection pressure.
**Action:** Use `any()` with a generator expression (`any(condition for task in tasks)`) instead of list comprehensions when only checking for existence of a condition, preventing O(N) list materialization.
