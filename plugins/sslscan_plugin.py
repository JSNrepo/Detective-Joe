#!/usr/bin/env python3
"""
SSLScan Plugin for Detective Joe v1.5
SSL/TLS security analysis using SSLScan tool.
"""

import re
from typing import Dict, Any, List
from plugins.base import PluginBase


class SSLScanPlugin(PluginBase):
    """Plugin for SSL/TLS analysis using SSLScan."""
    
    def __init__(self):
        super().__init__("sslscan", "1.0")
        self._tool_name = "sslscan"
        self._categories = ["website", "ip_server"]
        self._required_tools = ["sslscan"]
    
    @property
    def tool_name(self) -> str:
        return self._tool_name
    
    @property
    def categories(self) -> List[str]:
        return self._categories
    
    @property
    def required_tools(self) -> List[str]:
        return self._required_tools
    
    def build_command(self, target: str, category: str, **kwargs) -> str:
        """
        Build sslscan command for SSL/TLS analysis.
        
        Args:
            target: Domain or IP to analyze
            category: Investigation category
            **kwargs: Additional arguments (port, etc.)
        
        Returns:
            Command string for sslscan
        """
        port = kwargs.get("port", 443)
        
        # Remove protocol if present
        target = target.replace('https://', '').replace('http://', '')
        
        # Build sslscan command
        cmd = f"sslscan --no-color {target}:{port}"
        
        return cmd
    
    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse sslscan output to extract SSL/TLS information.
        
        Args:
            output: Raw command output
            target: Target domain/IP
            category: Investigation category
        
        Returns:
            Parsed data with SSL/TLS information and vulnerabilities
        """
        vulnerabilities = []
        certificates = []
        cipher_suites = {"accepted": [], "rejected": []}
        ssl_versions = {"supported": [], "unsupported": []}
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Check for vulnerabilities
            if 'vulnerable' in line_lower or 'weak' in line_lower:
                vulnerabilities.append(line.strip())
            
            # SSL/TLS version support
            if 'sslv2' in line_lower or 'sslv3' in line_lower or 'tlsv' in line_lower:
                if 'enabled' in line_lower or 'supported' in line_lower:
                    version = re.search(r'(SSLv[0-9]|TLSv[0-9]\.[0-9])', line, re.IGNORECASE)
                    if version:
                        ssl_versions["supported"].append(version.group(1))
                elif 'disabled' in line_lower or 'not supported' in line_lower:
                    version = re.search(r'(SSLv[0-9]|TLSv[0-9]\.[0-9])', line, re.IGNORECASE)
                    if version:
                        ssl_versions["unsupported"].append(version.group(1))
            
            # Cipher suites
            if 'accepted' in line_lower and 'cipher' in line_lower:
                cipher = line.strip()
                cipher_suites["accepted"].append(cipher)
            elif 'rejected' in line_lower and 'cipher' in line_lower:
                cipher = line.strip()
                cipher_suites["rejected"].append(cipher)
            
            # Certificate information
            if 'subject:' in line_lower or 'issuer:' in line_lower or 'not before:' in line_lower or 'not after:' in line_lower:
                certificates.append(line.strip())
        
        # Identify specific vulnerabilities
        known_vulns = []
        if any('sslv2' in v.lower() for v in ssl_versions["supported"]):
            known_vulns.append("SSLv2 is enabled (vulnerable to DROWN)")
        if any('sslv3' in v.lower() for v in ssl_versions["supported"]):
            known_vulns.append("SSLv3 is enabled (vulnerable to POODLE)")
        if any('tlsv1.0' in v.lower() or 'tlsv1.1' in v.lower() for v in ssl_versions["supported"]):
            known_vulns.append("TLSv1.0/1.1 enabled (deprecated, should upgrade)")
        
        vulnerabilities.extend(known_vulns)
        
        return {
            "target": target,
            "category": category,
            "vulnerabilities": vulnerabilities,
            "vulnerability_count": len(vulnerabilities),
            "ssl_versions_supported": ssl_versions["supported"],
            "ssl_versions_unsupported": ssl_versions["unsupported"],
            "accepted_ciphers": cipher_suites["accepted"],
            "accepted_cipher_count": len(cipher_suites["accepted"]),
            "certificates": certificates,
            "raw_output": output
        }
