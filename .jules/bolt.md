## 2024-03-14 - Replace O(N) list comprehension with any() generator in wait_for_tasks polling
**Learning:** Polling loops in `async_worker.py`'s `wait_for_tasks` use a full list comprehension to check pending tasks, generating an intermediate list on every 0.1s iteration. This wastes memory overhead.
**Action:** Replace the full list comprehension with `any(...)` generator expression to fast-fail on the first pending task without allocating a new list each time.
