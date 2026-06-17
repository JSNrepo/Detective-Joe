## 2026-06-17 - Command Injection in Nmap Plugin
**Vulnerability:** User-controlled inputs (target, ports, scripts) were interpolated directly into shell commands without sanitization in the Nmap plugin, allowing arbitrary command execution.
**Learning:** The async plugin architecture uses asyncio.create_subprocess_shell(), which is vulnerable to command injection if the inputs are not properly escaped. Even seemingly safe fields like 'target' or 'ports' can be manipulated to break out of the command.
**Prevention:** Always use shlex.quote(str(value)) to sanitize inputs before including them in shell commands. Ensure the output of shlex.quote() is not wrapped in manual quotes, as this defeats the escaping.
