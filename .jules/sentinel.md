## 2026-06-09 - Command Injection via Unsanitized Inputs in Nmap Plugin

**Vulnerability:** Shell command injection existed in `plugins/nmap_plugin.py` due to direct string concatenation of user-provided variables (`target`, `ports`, `timing`, `script`) into the command string executed by `asyncio.create_subprocess_shell`.

**Learning:** Any plugin using a `build_command` pattern that returns a raw shell string for execution is highly vulnerable to injection if inputs aren't escaped. Bandit's `subprocess_without_shell_equals_true` checks may not reliably flag logic that dynamically builds and later passes a string to an async shell execution method.

**Prevention:** Always use `shlex.quote(str(variable))` to sanitize *every* dynamic parameter before interpolating it into a shell string.
