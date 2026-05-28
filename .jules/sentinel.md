## 2026-05-28 - Command Injection via subprocess in Plugins
**Vulnerability:** The plugins were taking `target` and `kwargs` user input directly into f-strings representing bash commands. These strings were then run using `asyncio.create_subprocess_shell`, which meant malicious input like `; rm -rf /` would be executed.
**Learning:** `asyncio.create_subprocess_shell` executes standard shell strings. Standard string formatting without shell quoting allows users to break out of the string boundary and execute arbitrary commands.
**Prevention:** Always cast variables to string if necessary, and use `shlex.quote()` on all dynamic data points before inserting them into shell commands.
