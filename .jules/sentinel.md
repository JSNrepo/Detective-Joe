
## 2024-05-27 - [CRITICAL] Fix command injection in plugins
**Vulnerability:** Shell command injection via unsanitized user input in plugins.
**Learning:** Plugins passed unquoted variables like `target`, `ports`, etc., directly to `asyncio.create_subprocess_shell`. This is dangerous.
**Prevention:** Always use `shlex.quote(str(variable))` for dynamic string variables passed into shell commands, even if they seem trusted or simple.
