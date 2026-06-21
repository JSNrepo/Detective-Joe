## 2026-06-21 - Fix Insecure Deserialization
**Vulnerability:** Use of pickle for serializing state.
**Learning:** Pickle is inherently unsafe as it allows arbitrary code execution.
**Prevention:** Use secure serialization formats like JSON instead.
