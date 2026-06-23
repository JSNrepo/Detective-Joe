## $(date +"%Y-%m-%d") - Concurrent Async Refactoring
**Learning:** In sequential loops involving `await`, accumulating the coroutines in a list and processing them concurrently using `asyncio.gather(*tasks, return_exceptions=True)` dramatically reduces I/O wait time without changing behavior.
**Action:** Always scan `for` loops in asynchronous blocks to identify independent awaited network or database calls. When converting to concurrent batches, ensure task list initialization (`tasks = []`) occurs outside the loops and handle exceptions safely.
