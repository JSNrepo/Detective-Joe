## 2026-06-04 - Unhandled Command Injection in Plugin Framework
**Vulnerability:** Unhandled command injection vulnerabilities existed across the plugin framework where shell commands were being built using f-string interpolation with user-supplied inputs before executing them via `asyncio.create_subprocess_shell`.
**Learning:** This existed because raw user input variables (like targets, ports, config paths) were directly concatenated into strings destined for bash execution without quoting or sanitization, assuming trusted local use.
**Prevention:** To avoid this next time, consistently use `shlex.quote()` on any variable input that is concatenated into a shell command, or preferably execute via subprocess arrays instead of `shell=True`.
