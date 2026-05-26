## 2026-05-26 - Optimized Artifact Search
**Learning:** Checking against a subset of artifacts (`get_artifacts_by_type`) is much faster than iterating over all artifacts and comparing types for similarity checks.
**Action:** Always prefer subset iterators or lookup tables when finding similar items in a large dictionary/dataset.