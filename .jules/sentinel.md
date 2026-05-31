## 2026-05-25 - Fix command injection in asyncio subprocess shell calls
**Vulnerability:** Command injection vulnerability in the plugin architecture where user inputs (e.g., target, ports, arguments) were directly interpolated into shell commands via `asyncio.create_subprocess_shell`.
**Learning:** Shell interpolation without proper escaping allows an attacker to inject arbitrary shell commands if they control any of the interpolated variables.
**Prevention:** Always use `shlex.quote()` to sanitize user inputs before string interpolation into shell commands (like those executed via `asyncio.create_subprocess_shell`). Ensure `shlex.quote()` outputs are not wrapped in manual quotes.
