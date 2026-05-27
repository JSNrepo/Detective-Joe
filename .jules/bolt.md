## 2026-05-27 - Optimize artifact lookups using type indexes
**Learning:** Iterating over a full dictionary when secondary indexes (like `artifacts_by_type`) exist is an O(N) anti-pattern. Always use specific lookups to reduce search space to O(K).
**Action:** Replaced `self.artifacts.values()` iterations with `self.get_artifacts_by_type()` to optimize deduplication and chaining lookups.
