## 2026-06-21 - Concurrent Batching in Artifact Chaining
**Learning:** Sequential awaits inside nested loops bottlenecked the AsyncWorkerPool, preventing concurrent plugin execution for multiple targets.
**Action:** Use asyncio.gather with return_exceptions=True to run dynamically generated coroutines concurrently.
