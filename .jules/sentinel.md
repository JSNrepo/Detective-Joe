## 2026-06-01 - Command Injection in Plugin Framework
**Vulnerability:** Plugin framework constructed shell commands by interpolating unescaped user input (`target`, `ports`, etc.).
**Learning:** This exposes the tool to arbitrary command execution when invoking `asyncio.create_subprocess_shell`.
**Prevention:** Always use `shlex.quote()` when directly passing arguments to the shell in shell mode. Avoid shell=True where possible and use exec mode (list format) instead.
