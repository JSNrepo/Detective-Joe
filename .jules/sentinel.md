## 2026-06-03 - [Command Injection in Plugin Executions]
**Vulnerability:** Shell metacharacter injection in multiple plugins (`plugins/nmap_plugin.py`, `plugins/whois_plugin.py`, etc.).
**Learning:** Plugins were interpolating raw user inputs (like domain names or port targets) into shell commands that were executed through `asyncio.create_subprocess_shell`. This directly allows command injection if a user injects values like `target; rm -rf /`.
**Prevention:** Use `shlex.quote()` systematically on any variable going into a string representing a shell command, and avoid putting manual single quotes around variables wrapped in `shlex.quote()`.
