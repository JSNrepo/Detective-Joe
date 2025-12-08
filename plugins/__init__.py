#!/usr/bin/env python3
"""
Detective Joe v1.5 - Plugin Package
Plugin system for modular reconnaissance tool integration with auto-discovery.
"""

from .base import PluginBase
from .nmap_plugin import NmapPlugin
from .theharvester_plugin import TheHarvesterPlugin
from .sublist3r_plugin import Sublist3rPlugin
from .whatweb_plugin import WhatWebPlugin
from .sslscan_plugin import SSLScanPlugin
from .dnsrecon_plugin import DNSReconPlugin
from .whois_plugin import WhoisPlugin
from .discovery import PluginDiscovery, PluginManifest

__all__ = [
    'PluginBase',
    'NmapPlugin',
    'TheHarvesterPlugin',
    'Sublist3rPlugin',
    'WhatWebPlugin',
    'SSLScanPlugin',
    'DNSReconPlugin',
    'WhoisPlugin',
    'PluginDiscovery',
    'PluginManifest'
]