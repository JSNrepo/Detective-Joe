## 2026-06-12 - Artifact Chaining Concurrency
**Learning:** `_perform_artifact_chaining` sequentially awaited plugin tasks, resulting in high latency as each chained reconnaissance step (like nmap or whois on subdomains) blocked the execution of subsequent plugins for different artifacts or targets.
**Action:** Used `asyncio.gather(*coroutines, return_exceptions=True)` to execute all chained plugin reconnaissance commands concurrently. `return_exceptions=True` is critical to prevent a single target failure from aborting the entire chaining batch.
