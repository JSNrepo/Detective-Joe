## 2026-06-25 - Optimize polling loop with any() generator
**Learning:** The previous polling loop built a full list of pending tasks using a list comprehension on every 0.1s iteration, causing O(N) list allocations per cycle. Replacing this with an `any()` generator expression allows for immediate short-circuiting when a pending task is found, significantly reducing allocation overhead.
**Action:** When implementing polling mechanisms across a collection, use short-circuiting generator expressions like `any()` instead of full list comprehensions to minimize memory allocation and CPU cycles.
