## 2026-05-25 - Prevent Command Injection via Plugin Targets
**Vulnerability:** Many plugins pass the raw target input to OS shell via `asyncio.create_subprocess_shell` without proper escaping or sanitization.
**Learning:** `PluginBase.validate_target` previously only checked for truthiness, allowing attackers to inject metacharacters like `;`, `&`, `|` into the target (e.g. `example.com; rm -rf /`).
**Prevention:** Always validate against common shell metacharacters in base classes when arguments will eventually be executed in a shell environment, unless explicit functionality requires them.
