
## 2026-07-03 - Optimize polling with any()
**Learning:** Using list comprehensions in polling loops causes unnecessary O(N) memory allocations per cycle. Replacing it with `any()` and a generator expression prevents these allocations.
**Action:** Use `any()` generator expressions for polling task collections instead of list comprehensions to prevent O(N) memory allocations.
