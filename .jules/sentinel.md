
## 2026-07-03 - Fix command injection vulnerability in TOR service integration
**Vulnerability:** Use of `sh -c` combined with shell pipelines and string interpolation inside `subprocess.run` exposed the system to command injection.
**Learning:** Passing untrusted or concatenated input through shell pipelines inside Python avoids injection protections. `subprocess.run()` with `input` argument is much safer for handling payloads.
**Prevention:** Avoid `sh -c` and pipelines. Invoke target binaries directly and pass the payload securely via the `input` argument.
