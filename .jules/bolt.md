
## 2026-06-28 - Optimize Task Polling Memory Allocation
**Learning:** The `AsyncWorkerPool` in this codebase polls task states frequently (every 0.1s). Using full list comprehensions for state checks during these cycles creates unnecessary O(N) memory allocations, compounding garbage collection overhead.
**Action:** Always prefer `any()` generator expressions over list comprehensions when polling task collections in `async_worker.py` or similar tight polling loops to prevent intermediate list allocations.
