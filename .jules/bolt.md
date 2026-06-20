## 2026-06-20 - Concurrent Execution Optimization
**Learning:** Awaiting async tasks sequentially inside nested loops creates a performance bottleneck.
**Action:** Construct a list of coroutines and execute them concurrently using asyncio.gather() instead of sequentially waiting.
