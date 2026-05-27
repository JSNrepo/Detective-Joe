## 2025-05-27 - Plugin Architecture Command Injection

**Vulnerability:** The `build_command` method in plugins used unprotected f-strings to insert user-provided parameters (such as `target`, `ports`, `threads`, `scan_type`) into shell commands that are then executed via `asyncio.create_subprocess_shell`.
**Learning:** Shell metacharacters provided in user inputs could allow command injection if inputs are not properly sanitized or escaped when building shell commands.
**Prevention:** Always use `shlex.quote()` on any variable that will be interpolated into a string meant for shell execution. Avoid manual quotes around the result of `shlex.quote()`.
