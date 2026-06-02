## 2024-06-03 - [Fix Command Injection in Plugin Architecture]
**Vulnerability:** User inputs (like `target`, `ports`, `script`) were being directly string interpolated into shell commands in the `build_command` method of plugins, which are then executed via `asyncio.create_subprocess_shell()` in `plugins/base.py`. This allows for command injection.
**Learning:** Command injection is possible when unsanitized user inputs are passed into shell commands. The plugin architecture relies on string interpolation to build commands, making it susceptible to this vulnerability.
**Prevention:** Always use `shlex.quote()` to sanitize user inputs before string interpolation into shell commands. Ensure `shlex.quote()` outputs are not wrapped in manual quotes.
