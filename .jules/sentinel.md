## 2026-06-20 - Fix XXE and Insecure Deserialization
**Vulnerability:** XXE injection in minidom and insecure deserialization in pickle.
**Learning:** Using minidom to parse untrusted XML and pickle to deserialize untrusted data can lead to security breaches.
**Prevention:** Use defusedxml or ET.indent for XML, and stick to JSON for safe serialization.
