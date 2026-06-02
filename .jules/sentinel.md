## 2026-05-25 - Shell Command Injection in Plugins

**Vulnerability:** String interpolation was directly used to inject unvalidated arguments (like `target`, `ports`, `threads`, etc.) into shell commands (e.g., `asyncio.create_subprocess_shell`) across multiple plugins, allowing command injection.
**Learning:** Shell commands constructed via format strings are inherently vulnerable if user-controlled variables are not sanitized or safely quoted.
**Prevention:** Always use `shlex.quote()` on any variable being interpolated into a shell command to ensure it is interpreted solely as a single argument and safely escaped. Ensure `shlex.quote()` outputs are not wrapped in manual quotes.
