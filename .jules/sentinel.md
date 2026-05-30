## 2026-05-25 - [CRITICAL/HIGH] Fix Command Injection in Plugin Framework
**Vulnerability:** Command injection vulnerabilities existed in multiple reconnaissance plugins (nmap, dnsrecon, whois, etc.) because user-controlled parameters (target, ports, etc.) were interpolated directly into shell command strings without sanitization.
**Learning:** Shell commands constructed via f-strings are highly susceptible to injection if inputs aren't escaped properly.
**Prevention:** Always use `shlex.quote()` to sanitize user inputs before string interpolation into shell commands, or use list-based arguments with `subprocess.Popen` where possible instead of shell execution.
