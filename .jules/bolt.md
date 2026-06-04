## 2024-06-04 - Caching Disk I/O bound methods for plugin discovery
**Learning:** Checking the presence of multiple system commands (`shutil.which()`) sequentially within loops causes extreme performance bottlenecks due to repetitive I/O system calls and checking all PATH variables. The lookup time scales terribly.
**Action:** Always wrap methods performing disk I/O in simple cache decorators (`functools.lru_cache(maxsize=None)`) when the result is stateless and immutable during script execution (like the presence of binary tools).
