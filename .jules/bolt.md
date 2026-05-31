## 2026-05-31 - Replaced polling loop with Event in asyncio
**Learning:** Polling loops like `await asyncio.sleep(0.1)` to check task completion introduce unnecessary latency. `asyncio.Event` can be used to notify waiting tasks immediately without constant polling.
**Action:** Always use synchronization primitives like `asyncio.Event` or `asyncio.Condition` instead of polling when waiting for task completion.
