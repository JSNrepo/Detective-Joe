#!/usr/bin/env python3
"""
WhatWeb Plugin for Detective Joe v1.5
Web technology fingerprinting using WhatWeb tool.
"""

import re
import json
from typing import Dict, Any, List
from plugins.base import PluginBase


class WhatWebPlugin(PluginBase):
    """Plugin for web technology fingerprinting using WhatWeb."""
    
    def __init__(self):
        super().__init__("whatweb", "1.0")
        self._tool_name = "whatweb"
        self._categories = ["website"]
        self._required_tools = ["whatweb"]
    
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
        Build whatweb command for technology fingerprinting.
        
        Args:
            target: URL or domain to fingerprint
            category: Investigation category
            **kwargs: Additional arguments (aggression, verbosity, etc.)
        
        Returns:
            Command string for whatweb
        """
        aggression = kwargs.get("aggression", 1)
        
        # Ensure target has protocol
        if not target.startswith(('http://', 'https://')):
            target = f"http://{target}"
        
        # Build whatweb command - output to stdout for cross-platform compatibility
        # Note: This requires Unix-like systems. For Windows, temp file would be needed.
        cmd = f"whatweb -a {aggression} --color=never --log-json=- {target}"
        
        return cmd
    
    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse whatweb output to extract technology information.
        
        Args:
            output: Raw command output
            target: Target URL/domain
            category: Investigation category
        
        Returns:
            Parsed data with identified technologies
        """
        technologies = []
        web_servers = []
        frameworks = []
        cms_systems = []
        
        # Try to parse JSON output first
        try:
            # WhatWeb JSON output is one JSON object per line
            lines = output.strip().split('\n')
            for line in lines:
                if line.strip().startswith('{'):
                    data = json.loads(line)
                    plugins = data.get('plugins', {})
                    
                    for plugin_name, plugin_data in plugins.items():
                        tech_info = {
                            "name": plugin_name,
                            "version": plugin_data.get('version', [''])[0] if isinstance(plugin_data.get('version'), list) else plugin_data.get('version', ''),
                            "categories": plugin_data.get('categories', [])
                        }
                        
                        technologies.append(tech_info)
                        
                        # Categorize technologies
                        if 'web-server' in str(plugin_data).lower():
                            web_servers.append(plugin_name)
                        if 'framework' in str(plugin_data).lower():
                            frameworks.append(plugin_name)
                        if any(cms in plugin_name.lower() for cms in ['wordpress', 'joomla', 'drupal', 'cms']):
                            cms_systems.append(plugin_name)
        
        except json.JSONDecodeError:
            # Fallback to text parsing
            lines = output.strip().split('\n')
            for line in lines:
                # Extract technology names from text output
                if '[' in line and ']' in line:
                    matches = re.findall(r'\[([^\]]+)\]', line)
                    for match in matches:
                        # Parse version if present
                        parts = match.split(',')
                        tech_name = parts[0].strip()
                        version = ''
                        
                        for part in parts[1:]:
                            if 'Version' in part or 'v' in part:
                                version = part.strip()
                        
                        tech_info = {
                            "name": tech_name,
                            "version": version,
                            "categories": []
                        }
                        technologies.append(tech_info)
                        
                        # Categorize
                        tech_lower = tech_name.lower()
                        if any(server in tech_lower for server in ['apache', 'nginx', 'iis', 'server']):
                            web_servers.append(tech_name)
                        if any(fw in tech_lower for fw in ['laravel', 'django', 'rails', 'spring', 'express']):
                            frameworks.append(tech_name)
                        if any(cms in tech_lower for cms in ['wordpress', 'joomla', 'drupal']):
                            cms_systems.append(tech_name)
        
        # Remove duplicates
        web_servers = list(set(web_servers))
        frameworks = list(set(frameworks))
        cms_systems = list(set(cms_systems))
        
        return {
            "target": target,
            "category": category,
            "technologies": technologies,
            "technology_count": len(technologies),
            "web_servers": web_servers,
            "frameworks": frameworks,
            "cms_systems": cms_systems,
            "raw_output": output
        }
