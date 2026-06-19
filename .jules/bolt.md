## 2026-06-19 - Refactoring Async Loops
**Learning:** Artifact chaining was incorrectly using a sequential await pattern inside nested loops. This severely limited the concurrent potential of the AsyncWorkerPool and caused artificial delays. This is a common performance anti-pattern in async setups.
**Action:** Replaced sequential awaits inside loops with collecting coroutines and using `asyncio.gather(*tasks, return_exceptions=True)` to execute them concurrently, taking care to map the results back to their originating tasks.
