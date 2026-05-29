## 2024-05-29 - Systemic Command Injection Vulnerability

**Vulnerability:** Found a command injection vulnerability in `plugins/nmap_plugin.py` where user inputs (target, ports, timing, script) were being directly formatted into a shell command string that was executed using `asyncio.create_subprocess_shell`.
**Learning:** Shell strings constructed via string interpolation allow attackers to inject arbitrary commands using shell metacharacters (like `;`, `|`, `&&`). This was occurring because the framework passes the string to a shell, rather than an array to `subprocess.exec`.
**Prevention:** To prevent command injection vulnerabilities within the plugin architecture, always use `shlex.quote()` to sanitize user inputs (e.g., target, ports, arguments) before string interpolation into shell commands executed via `asyncio.create_subprocess_shell`. Ensure `shlex.quote()` outputs are not wrapped in manual quotes.
