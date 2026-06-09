## 2024-06-09 - [Execute async tasks concurrently instead of sequentially in loops]
**Learning:** In asynchronous loops, sequential `await`s completely defeat the purpose of asynchronous concurrency and throttle execution (like executing plugin batches one by one in `_perform_artifact_chaining`).
**Action:** Always accumulate coroutines into a list when iterating and executing tasks, then use `asyncio.gather(*coros)` to execute them concurrently for significant performance boosts in loop structures.
