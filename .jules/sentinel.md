## 2026-05-25 - Shell Command Injection in Plugin Framework
**Vulnerability:** User inputs (like `target`) were directly interpolated into shell commands passed to `asyncio.create_subprocess_shell` without sanitization.
**Learning:** Any dynamic shell command building must correctly quote inputs to avoid malicious shell execution.
**Prevention:** Always use `shlex.quote()` on user-controlled inputs before concatenating them into shell commands.
