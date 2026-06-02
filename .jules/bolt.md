## 2024-06-02 - Optimize Artifact Duplication Search
**Learning:** Found an `O(N)` search bottleneck during deduplication in `intelligence.py`, where N is the total number of artifacts. `find_similar_artifacts` iterated over all artifacts in the database regardless of type.
**Action:** Always leverage existing type indices (e.g., `artifacts_by_type`) to narrow the search space before comparing values.
