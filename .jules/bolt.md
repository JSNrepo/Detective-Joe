## 2026-06-18 - Concurrent Async Tasks
**Learning:** Sequential awaits in loops can block the event loop and degrade performance in async architectures.
**Action:** Always gather independent coroutines and use asyncio.gather(..., return_exceptions=True) for bulk concurrent execution.
