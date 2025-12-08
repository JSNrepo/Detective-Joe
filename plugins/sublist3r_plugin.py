#!/usr/bin/env python3
"""
Sublist3r Plugin for Detective Joe v1.5
Subdomain enumeration using Sublist3r tool.
"""

import re
from typing import Dict, Any, List
from plugins.base import PluginBase


class Sublist3rPlugin(PluginBase):
    """Plugin for subdomain enumeration using Sublist3r."""
    
    def __init__(self):
        super().__init__("sublist3r", "1.0")
        self._tool_name = "sublist3r"
        self._categories = ["website", "organisation"]
        self._required_tools = ["sublist3r"]
    
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
        Build sublist3r command for subdomain enumeration.
        
        Args:
            target: Domain to enumerate subdomains for
            category: Investigation category
            **kwargs: Additional arguments (threads, engines, etc.)
        
        Returns:
            Command string for sublist3r
        """
        threads = kwargs.get("threads", 10)
        
        # Basic sublist3r command
        cmd = f"sublist3r -d {target} -t {threads} -n"
        
        return cmd
    
    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse sublist3r output to extract subdomains.
        
        Args:
            output: Raw command output
            target: Target domain
            category: Investigation category
        
        Returns:
            Parsed data with discovered subdomains
        """
        subdomains = []
        
        # Extract subdomains from output
        # Sublist3r typically outputs one subdomain per line
        lines = output.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for domain patterns
            if '.' in line and target in line:
                # Clean up the line
                subdomain = line.split()[-1] if ' ' in line else line
                # Remove common prefixes
                subdomain = subdomain.replace('[-]', '').replace('[+]', '').strip()
                
                # Validate it's a proper subdomain
                if subdomain and '.' in subdomain and not subdomain.startswith('['):
                    subdomains.append(subdomain)
        
        # Remove duplicates while preserving order
        unique_subdomains = []
        seen = set()
        for subdomain in subdomains:
            if subdomain not in seen:
                seen.add(subdomain)
                unique_subdomains.append(subdomain)
        
        return {
            "target": target,
            "category": category,
            "subdomains": unique_subdomains,
            "subdomain_count": len(unique_subdomains),
            "raw_output": output
        }
