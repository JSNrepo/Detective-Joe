
## 2026-06-24 - Async Worker Pool Starvation
**Learning:** Sequential execution of batched tasks in loops starves the worker pool.
**Action:** Use asyncio.gather to schedule tasks concurrently.
