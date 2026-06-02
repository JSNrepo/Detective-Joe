## 2026-06-02 - Command Injection in Plugin Architecture
**Vulnerability:** Shell command execution without sanitization in plugin build_command functions.
**Learning:** `asyncio.create_subprocess_shell` combined with f-strings allows arbitrary command injection if any variable can be user-controlled.
**Prevention:** Always cast variables to strings and sanitize with `shlex.quote(str(var))` before inserting them into a shell command.
