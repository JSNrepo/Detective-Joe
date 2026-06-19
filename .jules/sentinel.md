## 2026-05-25 - [B113 Missing Requests Timeout]
**Vulnerability:** A requests.get() call in anonymity.py was made without an explicit timeout parameter.
**Learning:** Bandit cannot reliably evaluate inline .pop() methods or complex expressions for the B113 check. A missing timeout can cause a server process or worker thread to hang indefinitely if a request is unresponsive.
**Prevention:** Always explicitly pop the timeout value into a dedicated variable *before* passing it to the requests method to ensure Bandit cleanly passes and the connection handles timeouts securely.
