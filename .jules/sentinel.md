## 2024-05-27 - Command Injection via unescaped string interpolation in shell subprocess

**Vulnerability:**
Multiple reconnaissance plugins dynamically built shell commands using python f-strings directly with unsanitized user inputs, such as `f"nmap {target}"`. These commands were then executed through `asyncio.create_subprocess_shell()`. An attacker could exploit this by providing a target like `"example.com; rm -rf /"` to execute arbitrary shell commands.

**Learning:**
Passing a raw string built with user input to a shell execution function (like `create_subprocess_shell`, `os.system`, or `subprocess.Popen(..., shell=True)`) is highly dangerous because the shell parses and evaluates operators like `;`, `&&`, `||`, and backticks.

**Prevention:**
Always use `shlex.quote()` when interpolating variables into a command string destined for the shell. Alternatively, execute external processes by passing an argument array to functions that do not spawn a shell (like `asyncio.create_subprocess_exec()`), avoiding shell injection risks entirely.
