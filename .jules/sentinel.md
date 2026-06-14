## 2024-05-18 - Command Injection Vulnerability in Plugin Architecture
**Vulnerability:** The plugin architecture uses `asyncio.create_subprocess_shell` with untrusted target arguments directly interpolated via f-strings. This allows an attacker to inject shell commands via the target parameter (e.g. `target; malicious_command`).
**Learning:** Shell subprocess execution (`shell=True` or `create_subprocess_shell`) is risky when incorporating unvalidated input.
**Prevention:** All inputs incorporated into shell commands must be sanitized using `shlex.quote(str(value))` to prevent command injection.
