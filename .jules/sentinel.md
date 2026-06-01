## 2024-06-01 - Command Injection in Plugin Framework
**Vulnerability:** Unsanitized user inputs (`target`, and kwargs like `ports`, `script`, `timing`) are directly interpolated into shell command strings in `plugins/nmap_plugin.py` and executed via `asyncio.create_subprocess_shell`.
**Learning:** Even with basic input validation in `validate_target` (which checks for some special chars), command injection is still possible if variables aren't properly escaped before passing to a shell. The framework passes user input directly to subprocess execution.
**Prevention:** Always use `shlex.quote()` on all user-supplied data (target, ports, script arguments) before interpolating into shell commands, or avoid `shell=True` and pass arguments as a list.
