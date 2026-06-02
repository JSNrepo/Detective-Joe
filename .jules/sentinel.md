## 2026-06-02 - Prevent Command Injection in Plugins
**Vulnerability:** Plugin architecture lacked input sanitization when constructing shell commands for `asyncio.create_subprocess_shell`.
**Learning:** Raw user inputs (`target` and `kwargs`) were being directly interpolated into shell commands via f-strings, leading to potential command injection.
**Prevention:** Always use `shlex.quote()` on user inputs before injecting them into shell commands. Ensure outputs are not wrapped in manual quotes.
