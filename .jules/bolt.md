## 2026-06-19 - Refactored sequential plugin execution into concurrent batches
**Learning:** Sequential async executions inside nested loops limit throughput, especially during recursive artifact chaining where tasks share no interdependent state.
**Action:** Replaced sequential awaits inside a loop with a queued task list execution via `asyncio.gather(*tasks, return_exceptions=True)` to dramatically improve fan-out concurrency.
