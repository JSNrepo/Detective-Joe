## 2026-06-20 - [Command Injection in Plugin Architecture]
**Vulnerability:** Command injection vulnerability (CWE-78) where unsanitized user inputs were interpolated directly into shell commands in plugins like NmapPlugin.
**Learning:** The plugin architecture uses string interpolation for arguments which are then passed to `asyncio.create_subprocess_shell`. Because shell operators like `;` or `&` were not escaped, a malicious target or argument could execute arbitrary commands.
**Prevention:** To prevent command injection vulnerabilities within the plugin architecture, always use `shlex.quote()` to sanitize user inputs (e.g., target, ports, arguments) before string interpolation into shell commands. Ensure `shlex.quote()` outputs are not wrapped in manual quotes.
