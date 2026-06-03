## 2026-05-25 - Fix Command Injection in Plugin Architecture
**Vulnerability:** Command injection in multiple reconnaissance plugins.
**Learning:** External user inputs were being directly interpolated into shell command strings execution by `create_subprocess_shell`. This bypassed shell sanitization completely.
**Prevention:** Always wrap external inputs using `shlex.quote()` before inserting them into shell commands. This securely escapes characters, thwarting shell-injection payload attacks.