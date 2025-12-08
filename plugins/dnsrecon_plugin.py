#!/usr/bin/env python3
"""
DNSRecon Plugin for Detective Joe v1.5
DNS enumeration using DNSRecon tool.
"""

import re
import json
from typing import Dict, Any, List
from plugins.base import PluginBase


class DNSReconPlugin(PluginBase):
    """Plugin for DNS enumeration using DNSRecon."""
    
    def __init__(self):
        super().__init__("dnsrecon", "1.0")
        self._tool_name = "dnsrecon"
        self._categories = ["website", "organisation", "ip_server"]
        self._required_tools = ["dnsrecon"]
    
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
        Build dnsrecon command for DNS enumeration.
        
        Args:
            target: Domain to enumerate
            category: Investigation category
            **kwargs: Additional arguments (type, threads, etc.)
        
        Returns:
            Command string for dnsrecon
        """
        scan_type = kwargs.get("type", "std")  # std, rvl, brt, srv, axfr, etc.
        
        # Build dnsrecon command - try JSON output first, fallback to text
        # Note: JSON output is parsed in Python, not relying on shell operators
        cmd = f"dnsrecon -d {target} -t {scan_type} -j -"
        
        return cmd
    
    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse dnsrecon output to extract DNS information.
        
        Args:
            output: Raw command output
            target: Target domain
            category: Investigation category
        
        Returns:
            Parsed data with DNS records and enumeration results
        """
        dns_records = {
            "A": [],
            "AAAA": [],
            "MX": [],
            "NS": [],
            "TXT": [],
            "SOA": [],
            "CNAME": [],
            "PTR": []
        }
        subdomains = []
        nameservers = []
        mail_servers = []
        
        # Try to parse JSON output first
        try:
            # DNSRecon may output multiple JSON objects
            json_objs = []
            for line in output.strip().split('\n'):
                if line.strip().startswith('[') or line.strip().startswith('{'):
                    try:
                        data = json.loads(line)
                        if isinstance(data, list):
                            json_objs.extend(data)
                        else:
                            json_objs.append(data)
                    except json.JSONDecodeError:
                        continue
            
            for record in json_objs:
                record_type = record.get('type', '')
                name = record.get('name', '')
                address = record.get('address', '') or record.get('target', '')
                
                if record_type in dns_records:
                    dns_records[record_type].append({
                        "name": name,
                        "value": address
                    })
                
                # Extract specific information
                if record_type == 'NS':
                    nameservers.append(address)
                elif record_type == 'MX':
                    mail_servers.append(address)
                
                # Collect subdomains
                if name and name != target and target in name:
                    subdomains.append(name)
        
        except (json.JSONDecodeError, ValueError):
            # Fallback to text parsing
            lines = output.strip().split('\n')
            
            for line in lines:
                # Parse different record types
                if 'A ' in line or 'AAAA ' in line:
                    match = re.search(r'(\S+)\s+\d+\s+IN\s+(A|AAAA)\s+(\S+)', line)
                    if match:
                        name, record_type, address = match.groups()
                        dns_records[record_type].append({
                            "name": name,
                            "value": address
                        })
                        if name != target and target in name:
                            subdomains.append(name)
                
                elif ' MX ' in line:
                    match = re.search(r'(\S+)\s+\d+\s+IN\s+MX\s+\d+\s+(\S+)', line)
                    if match:
                        name, mx_server = match.groups()
                        dns_records["MX"].append({
                            "name": name,
                            "value": mx_server
                        })
                        mail_servers.append(mx_server)
                
                elif ' NS ' in line:
                    match = re.search(r'(\S+)\s+\d+\s+IN\s+NS\s+(\S+)', line)
                    if match:
                        name, ns_server = match.groups()
                        dns_records["NS"].append({
                            "name": name,
                            "value": ns_server
                        })
                        nameservers.append(ns_server)
                
                elif ' TXT ' in line:
                    match = re.search(r'(\S+)\s+\d+\s+IN\s+TXT\s+"([^"]+)"', line)
                    if match:
                        name, txt_value = match.groups()
                        dns_records["TXT"].append({
                            "name": name,
                            "value": txt_value
                        })
                
                elif ' CNAME ' in line:
                    match = re.search(r'(\S+)\s+\d+\s+IN\s+CNAME\s+(\S+)', line)
                    if match:
                        name, cname_target = match.groups()
                        dns_records["CNAME"].append({
                            "name": name,
                            "value": cname_target
                        })
                        if name != target and target in name:
                            subdomains.append(name)
        
        # Remove duplicates
        subdomains = list(set(subdomains))
        nameservers = list(set(nameservers))
        mail_servers = list(set(mail_servers))
        
        return {
            "target": target,
            "category": category,
            "dns_records": dns_records,
            "subdomains": subdomains,
            "subdomain_count": len(subdomains),
            "nameservers": nameservers,
            "mail_servers": mail_servers,
            "raw_output": output
        }
