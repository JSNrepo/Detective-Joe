## 2024-05-31 - Command Injection in Plugins
**Vulnerability:** Command injection in `plugins/` directory. Target and argument inputs were directly formatted into shell strings in `build_command` implementations and executed via `asyncio.create_subprocess_shell`.
**Learning:** Plugins accepting arbitrary input should always sanitize them. Relying on basic string formatting allows attackers to append arbitrary shell commands (e.g. `; rm -rf /`).
**Prevention:** Use `shlex.quote()` on all dynamic inputs before interpolating them into a shell command string. Do not wrap the `shlex.quote()` output in extra quotes.
