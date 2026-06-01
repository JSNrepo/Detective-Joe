## 2026-06-01 - Command Injection in Plugins

**Vulnerability:** Shell command injection vulnerability exists across the plugin architecture due to unescaped user inputs (e.g. `target`, `ports`, `scan_type`) being concatenated directly into the shell commands executed via `asyncio.create_subprocess_shell`.

**Learning:** When using async task execution directly calling shell commands with external arguments, we must properly quote external parameters, especially when allowing arbitrary strings for hostnames or domain targets that could be exploited to escape command bounds.

**Prevention:** To prevent command injection vulnerabilities within the plugin architecture, always use `shlex.quote()` to sanitize user inputs (e.g., target, ports, arguments) before string interpolation into shell commands (like those executed via `asyncio.create_subprocess_shell`). Ensure `shlex.quote()` outputs are not wrapped in manual quotes.