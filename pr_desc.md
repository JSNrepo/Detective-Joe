---
# Daily Codebase Improvement Log: 2026-06-27

## 💡 What I Discovered & Idea Generated
I discovered that the task polling loop in `async_worker.py` used a full list comprehension to check for pending tasks, which causes an O(N) memory allocation per polling cycle.

## 🛠️ What I Fixed / Added
I refactored the pending tasks check in `async_worker.py` to use an `any()` generator expression instead of a list comprehension, preventing unnecessary memory allocations while polling.

## 🎯 Next Recommended Target
The `active_tasks` count on line 323 of `async_worker.py` also uses a full list comprehension (`len([t for t in self.tasks.values() if t.status == TaskStatus.RUNNING])`) instead of a generator with `sum()`. This should be optimized next.
---
