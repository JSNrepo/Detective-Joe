#!/usr/bin/env python3
"""
WHOIS Plugin for Detective Joe v1.5
Domain registration and ownership information using WHOIS.
"""

import re
from typing import Dict, Any, List
from datetime import datetime
from plugins.base import PluginBase


class WhoisPlugin(PluginBase):
    """Plugin for WHOIS lookups."""
    
    def __init__(self):
        super().__init__("whois", "1.0")
        self._tool_name = "whois"
        self._categories = ["website", "organisation"]
        self._required_tools = ["whois"]
    
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
        Build whois command for domain lookup.
        
        Args:
            target: Domain to lookup
            category: Investigation category
            **kwargs: Additional arguments
        
        Returns:
            Command string for whois
        """
        # Remove protocol if present
        target = target.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Build whois command
        cmd = f"whois {target}"
        
        return cmd
    
    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse whois output to extract registration information.
        
        Args:
            output: Raw command output
            target: Target domain
            category: Investigation category
        
        Returns:
            Parsed data with domain registration information
        """
        registrar = None
        nameservers = []
        creation_date = None
        expiration_date = None
        updated_date = None
        registrant = {}
        admin_contact = {}
        tech_contact = {}
        
        lines = output.strip().split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Extract registrar
            if 'registrar:' in line_lower or 'registrar name:' in line_lower:
                registrar = line.split(':', 1)[1].strip()
            
            # Extract nameservers
            if 'name server:' in line_lower or 'nserver:' in line_lower:
                ns = line.split(':', 1)[1].strip()
                nameservers.append(ns)
            
            # Extract dates
            if 'creation date:' in line_lower or 'created:' in line_lower:
                date_str = line.split(':', 1)[1].strip()
                creation_date = self._parse_date(date_str)
            
            if 'expiration date:' in line_lower or 'registry expiry date:' in line_lower or 'expires:' in line_lower:
                date_str = line.split(':', 1)[1].strip()
                expiration_date = self._parse_date(date_str)
            
            if 'updated date:' in line_lower or 'last updated:' in line_lower or 'changed:' in line_lower:
                date_str = line.split(':', 1)[1].strip()
                updated_date = self._parse_date(date_str)
            
            # Extract contact information
            if 'registrant' in line_lower and ':' in line:
                key = 'registrant_' + line.split(':')[0].strip().lower().replace(' ', '_')
                value = line.split(':', 1)[1].strip()
                registrant[key] = value
            
            if 'admin' in line_lower and ':' in line and 'email' not in line_lower:
                key = 'admin_' + line.split(':')[0].strip().lower().replace(' ', '_')
                value = line.split(':', 1)[1].strip()
                admin_contact[key] = value
            
            if 'tech' in line_lower and ':' in line and 'email' not in line_lower:
                key = 'tech_' + line.split(':')[0].strip().lower().replace(' ', '_')
                value = line.split(':', 1)[1].strip()
                tech_contact[key] = value
        
        # Remove duplicates from nameservers
        nameservers = list(set(nameservers))
        
        # Calculate domain age if creation date available
        domain_age_days = None
        if creation_date:
            try:
                age = datetime.now() - datetime.strptime(creation_date.split()[0], '%Y-%m-%d')
                domain_age_days = age.days
            except (ValueError, IndexError):
                pass
        
        return {
            "target": target,
            "category": category,
            "registrar": registrar,
            "nameservers": nameservers,
            "creation_date": creation_date,
            "expiration_date": expiration_date,
            "updated_date": updated_date,
            "domain_age_days": domain_age_days,
            "registrant": registrant,
            "admin_contact": admin_contact,
            "tech_contact": tech_contact,
            "raw_output": output
        }
    
    def _parse_date(self, date_str: str) -> str:
        """Parse various date formats from WHOIS output."""
        # Try common date patterns
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2024-01-15
            r'\d{2}/\d{2}/\d{4}',  # 01/15/2024
            r'\d{2}\.\d{2}\.\d{4}',  # 15.01.2024
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                return match.group(0)
        
        # Return original if no pattern matches
        return date_str.split()[0] if date_str else None
