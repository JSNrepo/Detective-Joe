# Detective Joe v1.5 — Next-Gen Recon Framework

[![Kali Linux Compatible](https://img.shields.io/badge/Kali%20Linux-Compatible-blue.svg)](https://www.kali.org/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📌 Overview
Detective Joe (**DJ**) v1.5 is a **next-generation automated reconnaissance framework** built for security professionals and researchers. Instead of running individual tools one by one, DJ chains reconnaissance tools through an async plugin architecture, executes them efficiently in parallel, and merges results into comprehensive, structured reports.

**Think of DJ as your intelligent recon operator** — you define the target and profile once, it handles the orchestration, execution, and analysis.

### 🎯 Why Detective Joe for Kali Linux?

**Problem**: Running multiple reconnaissance tools manually is time-consuming, error-prone, and makes correlation difficult.

**Solution**: Detective Joe automates and orchestrates your reconnaissance workflow:
- ✅ **One Command, Multiple Tools**: Run 8+ reconnaissance tools with a single command
- ✅ **AI-Powered Analysis**: Automated vulnerability correlation and risk assessment
- ✅ **MITRE ATT&CK Mapping**: Understand your reconnaissance activities in the ATT&CK framework
- ✅ **Kali-Optimized**: Designed for Kali Linux with all common tools pre-configured
- ✅ **Export Anywhere**: 5 output formats (TXT, HTML, JSON, CSV, XML) for any workflow
- ✅ **Zero Noise**: Intelligent parsing eliminates tool output noise, showing only what matters

**Perfect for**:
- 🔍 Penetration testers who need fast, comprehensive reconnaissance
- 🛡️ Security researchers performing OSINT investigations  
- 👨‍💻 Bug bounty hunters hunting for attack surface
- 🏢 Red teams conducting infrastructure assessments
- 📚 Students learning reconnaissance methodologies

---

## 🚀 v1.5 Features

### Core Framework Capabilities
- **🔄 Async Worker Pool**: Parallel task execution with configurable worker limits
- **🧩 Plugin Architecture**: Modular, extensible plugin system for reconnaissance tools
- **⚙️ Profile System**: Configurable investigation profiles (quick, standard, deep, custom)
- **🖥️ Dual Interface**: Both CLI arguments and interactive menu support
- **📊 Structured Reports**: TXT reports with parsed data and execution statistics
- **💾 State Management**: Caching, state persistence, and execution history

### Investigation Categories
- 🌐 **Website Investigation**: Domain analysis, subdomain discovery, web security
- 🏢 **Organisation Investigation**: Company intelligence, employee discovery, infrastructure mapping  
- 👤 **People Investigation**: OSINT on individuals, social media presence, contact discovery
- 🖥️ **IP / Server Investigation**: Network analysis, service detection, vulnerability assessment

### Built-in Plugins
- **Nmap Plugin**: Network scanning with intelligent command building
- **theHarvester Plugin**: Email harvesting and OSINT data collection
- **Sublist3r Plugin**: Subdomain enumeration and discovery
- **WhatWeb Plugin**: Web technology fingerprinting and identification
- **SSLScan Plugin**: SSL/TLS security analysis and vulnerability detection
- **DNSRecon Plugin**: Comprehensive DNS enumeration and zone transfer testing
- **WHOIS Plugin**: Domain registration and ownership information gathering
- **Demo Plugin**: Testing mode without external dependencies

### AI-Powered Intelligence Analysis (New!)
- **Google Gemini 2.5 Flash Integration**: FREE AI-powered reconnaissance analysis
- **Intelligent Risk Assessment**: Context-aware risk scoring and classification
- **Advanced Vulnerability Detection**: AI-driven identification of security issues with CVE correlation
- **Natural Language Insights**: Human-readable security summaries and recommendations
- **Attack Surface Analysis**: Comprehensive evaluation and quantification of exposed assets
- **Smart Recommendations**: Context-aware, prioritized security guidance
- **Executive Summaries**: Professional reports ready for stakeholders
- **Automated Threat Assessment**: AI-driven risk scoring and vulnerability correlation
- **MITRE ATT&CK Mapping**: Automatic mapping of reconnaissance activities to ATT&CK framework
- **CVE Correlation**: Automatic linking of identified vulnerabilities to CVE database

### Export Capabilities
- **Multiple Formats**: TXT, HTML, JSON, CSV, XML export support
- **Industry Standards**: CSV and XML formats for integration with other security tools
- **Structured Data**: Machine-readable outputs for automation and orchestration

---

## 🏗️ v1.5 Technical Architecture

### Directory Structure
```
detective-joe/
├── detectivejoe.py          # Main CLI script with async execution
├── config.py                # Legacy tool configurations (v1 compatibility)
├── profiles.yaml            # Investigation profiles and settings
├── async_worker.py          # Async worker pool implementation
├── intelligence.py          # Intelligence engine for artifact management
├── reports.py               # Multi-format report generators (TXT/HTML/JSON)
├── state_manager.py         # State persistence and resume functionality
├── anonymity.py             # TOR/proxy/UA rotation for anonymous recon
├── requirements.txt         # Python dependencies
├── plugins/                 # Plugin architecture
│   ├── __init__.py         #   Plugin package initialization
│   ├── base.py             #   Base plugin class and interface
│   ├── discovery.py        #   Plugin auto-discovery and manifest system
│   ├── nmap.yml            #   Nmap plugin manifest
│   ├── nmap_plugin.py      #   Nmap reconnaissance plugin
│   ├── theharvester.yml    #   theHarvester plugin manifest
│   └── theharvester_plugin.py #  theHarvester OSINT plugin
├── reports/                 # Generated investigation reports
├── cache/                   # Cached tool outputs and results
├── state/                   # Framework state and execution logs
│   └── intelligence/       #   Artifact database and intelligence files
├── tests/                   # Test infrastructure
│   └── test_framework.py   #   Comprehensive test suite
└── README.md               # This documentation
```

### Plugin System Architecture
```python
# Plugin Interface
class PluginBase(ABC):
    @abstractmethod
    async def execute(target, category, **kwargs) -> Dict[str, Any]
    @abstractmethod  
    def build_command(target, category, **kwargs) -> str
    @abstractmethod
    def parse_output(output, target, category) -> Dict[str, Any]
```

### Plugin Auto-Discovery
```yaml
# Plugin Manifest (plugins/example.yml)
name: "plugin_name"
version: "1.0"
description: "Plugin description"
tool_name: "underlying_tool"
required_tools: ["tool1", "tool2"]
categories: ["website", "organisation"]
plugin_class: "PluginClassName"
module_path: "plugin_module"
artifacts:
  produces: ["emails", "domains", "ips"]
  consumes: ["domains", "organizations"]
chain_priority: 1
tags: ["osint", "recon"]
```

### Intelligence Engine Architecture
```python
# Artifact Management
class Artifact:
    id: str
    type: str  # email, domain, ip, port, service, etc.
    value: str
    source_plugin: str
    confidence: float
    tags: List[str]
    metadata: Dict[str, Any]

# Intelligence Processing
- Automatic artifact extraction from plugin results
- Deduplication based on type and value
- CVE enrichment for services and vulnerabilities  
- Confidence scoring and metadata enrichment
- Persistent storage with JSON and binary formats
```

### Async Execution Model
- **Worker Pool**: Configurable number of parallel workers
- **Task Queue**: Async task distribution and load balancing  
- **Timeout Handling**: Per-task and global timeout management
- **Result Aggregation**: Structured result collection and formatting

---

## 📥 Installation

### 🚀 Automated Setup (Recommended)
The easiest way to set up Detective Joe, especially on Kali Linux and systems with PEP 668 restrictions:

```bash
git clone https://github.com/vinothvbt/Detective-Joe.git
cd Detective-Joe
chmod +x setup.sh
./setup.sh
```

The setup script will:
- ✅ Check Python 3 and pip availability
- ✅ Create a virtual environment in `.venv/`
- ✅ Install all requirements safely (including Gemini AI)
- ✅ Provide clear next steps

### 🤖 AI Configuration (Recommended)

Detective Joe now includes **FREE** AI-powered analysis using Google Gemini 2.5 Flash!

```bash
# Get your free API key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your-api-key-here"

# Or add to your shell config for persistence
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
```

**Features with AI enabled:**
- 🎯 Intelligent risk assessment and scoring
- 🔍 Advanced vulnerability detection with CVE correlation
- 📊 Comprehensive attack surface analysis
- 💡 Context-aware security recommendations
- 📝 Professional executive summaries

See [AI_INTEGRATION.md](AI_INTEGRATION.md) for detailed setup and usage.

After setup, always activate the virtual environment before using Detective Joe:
```bash
source .venv/bin/activate
python3 detectivejoe.py --help
```

### 🔧 Manual Setup
For manual installation or if you prefer to manage dependencies yourself:

```bash
git clone https://github.com/vinothvbt/Detective-Joe.git
cd Detective-Joe

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Make script executable
chmod +x detectivejoe.py
```

**Important for Kali Linux users:** Due to PEP 668 externally-managed-environment restrictions, Detective Joe **requires** a virtual environment. The automated setup handles this automatically.

### System Dependencies
Detective Joe v1.5 leverages existing reconnaissance tools. Install the following for full functionality:

**Kali Linux (recommended):**
```bash
sudo apt update
sudo apt install nmap theharvester sublist3r whatweb sslscan dnsrecon whois
```

**Or use our automated tool installer:**
```bash
# One-command installation of all tools
sudo ./install_tools.sh

# This script will:
# ✓ Install all required reconnaissance tools
# ✓ Verify installations
# ✓ Report any missing dependencies
```

**Individual Tool Installation:**
```bash
# Core scanning tools (usually pre-installed on Kali)
sudo apt install nmap whois dnsrecon sslscan

# Python-based tools
sudo apt install theharvester sublist3r whatweb

# Alternative: Install via pip
pip install theHarvester sublist3r

# Note: Some tools may need to be installed from GitHub
# git clone https://github.com/laramies/theHarvester && cd theHarvester && pip install -r requirements.txt
```

**Other Linux distributions:**
```bash
# Ubuntu/Debian
sudo apt install nmap whois dnsutils sslscan

# Fedora/RHEL
sudo dnf install nmap whois bind-utils

# macOS
brew install nmap

# For Python tools, use pip in the virtual environment
```

### 🚀 Quick Start with Demo Mode
If you want to test Detective Joe immediately without installing external tools:

```bash
# After setup, try the demo mode
source .venv/bin/activate
python3 detectivejoe.py -c website -t example.com -p demo
```

The demo profile uses basic system tools (curl, echo) to demonstrate the framework without requiring nmap or theharvester. This is perfect for:
- ✅ Testing the framework functionality
- ✅ Understanding the report generation
- ✅ Learning the command structure
- ✅ CI/CD environments

---

## ▶️ Usage

### CLI Mode (New in v1.5)
```bash
# 🚀 Demo mode - works without external tools
python3 detectivejoe.py -c website -t example.com -p demo

# Website investigation using standard profile
python3 detectivejoe.py -c website -t example.com

# Deep organisation scan with custom workers
python3 detectivejoe.py -c organisation -t company.com -p deep --workers 8

# Quick IP investigation with custom timeout
python3 detectivejoe.py -c ip -t 192.168.1.1 -p quick --timeout 60

# Stealth investigation with anonymity
python3 detectivejoe.py -c website -t example.com -p stealth

# List available profiles and plugins
python3 detectivejoe.py --list-profiles
python3 detectivejoe.py --list-plugins
```

### State Management
```bash
# Resume interrupted investigation
python3 detectivejoe.py --resume investigation_id

# List saved states
python3 detectivejoe.py --list-states

# Kill active investigation (Ctrl+C also works)
python3 detectivejoe.py --kill
```

### Interactive Mode (Enhanced)
```bash
python3 detectivejoe.py --interactive
```

Example CLI Session:
```
$ python3 detectivejoe.py -c website -t example.com -p standard

╔══════════════════════════════════════════════════════════════╗
║                    DETECTIVE JOE v1.5                       ║
║                 Next-Gen Recon Framework                     ║
║                                                              ║
║  Profile: standard           Workers: 4                      ║
║  Async Execution │ Plugin Architecture │ CLI & Interactive   ║
╚══════════════════════════════════════════════════════════════╝

[*] Starting website investigation for: example.com
[*] Using profile: standard
[*] Executing 2 plugins: ['nmap', 'theharvester']
[*] Processing 15 artifacts through intelligence engine
[*] Performing artifact chaining with depth 2
[*] Chained 3 additional tasks from discovered targets

======================================================================
AI-POWERED INTELLIGENCE ANALYSIS
Powered by Google Gemini 2.5 Flash
======================================================================

OVERALL RISK LEVEL: HIGH (Score: 68/100)

The target presents significant security concerns including outdated SSL/TLS 
configurations and exposed administrative services. Immediate action required 
to address critical vulnerabilities.

[✓] Investigation completed successfully!
[✓] TXT report saved: reports/example.com_website_2025-01-15_14-30-45.txt
[✓] HTML report saved: reports/example.com_website_2025-01-15_14-30-45.html
[✓] JSON report saved: reports/example.com_website_2025-01-15_14-30-45.json

SUMMARY:
  Tasks executed: 5
  Success rate: 100.0%
  Total time: 45.23s
  Artifacts found: 15
  Chained tasks: 3
```

---

## 🤖 AI-Powered Intelligence Features

### Gemini 2.5 Flash Integration (FREE!)

Detective Joe now includes intelligent analysis powered by Google's Gemini 2.5 Flash AI:

**Quick Setup:**
```bash
# Get your free API key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your-api-key-here"

# Run any scan - AI analysis is automatic!
python3 detectivejoe.py -c website -t example.com
```

**AI-Enhanced Report Example:**
```
======================================================================
AI-POWERED INTELLIGENCE ANALYSIS
Powered by Google Gemini 2.5 Flash
======================================================================

OVERALL RISK LEVEL: HIGH (Score: 68/100)

KEY FINDINGS:
  • Discovered 12 subdomain(s)
  • Identified 8 open port(s) including high-risk services
  • Found 3 high/critical severity vulnerabilities
  • Exposed administrative interfaces to public internet

IDENTIFIED VULNERABILITIES: 5
  [HIGH] Outdated SSL/TLS: SSLv3 enabled (CVE-2014-3566 POODLE)
  [HIGH] Remote Desktop (3389) publicly accessible
  [MEDIUM] WordPress 5.2 detected (outdated, known vulnerabilities)
  [MEDIUM] Deprecated TLS 1.0/1.1 protocols enabled

ATTACK SURFACE ANALYSIS:
  • Subdomains: 12 (potential takeover candidates)
  • Open Ports: 8 (including 3389, 445, 22)
  • Services: 5 (SSH, RDP, SMB, HTTP, HTTPS)
  • Exposed Emails: 3 (social engineering risk)

POTENTIAL ATTACK VECTORS:
  • Network service exploitation (RDP brute force)
  • SSL/TLS downgrade attacks (POODLE, BEAST)
  • Subdomain takeover opportunities
  • WordPress vulnerabilities and plugins
  • Social engineering via exposed contacts

TOP RECOMMENDATIONS:
  1. URGENT: Disable SSLv3, enable only TLS 1.2+
  2. URGENT: Restrict RDP (3389) to trusted IPs only
  3. HIGH: Update WordPress to latest version (6.4+)
  4. MEDIUM: Implement Web Application Firewall (WAF)
  5. MEDIUM: Review and secure/remove unused subdomains
  6. Enable security headers (HSTS, CSP, X-Frame-Options)

MITRE ATT&CK TECHNIQUES OBSERVED:
  • T1590.001 - Gather Victim Network Information: Domain Properties
  • T1046 - Network Service Scanning
  • T1590.002 - Gather Victim Network Information: DNS
======================================================================
```

**Benefits:**
- 🎯 **Context-Aware Analysis**: AI understands relationships between findings
- 🔍 **Smart Prioritization**: Recommendations ranked by actual risk and impact
- 📝 **Professional Reports**: Stakeholder-ready summaries and technical details
- 💡 **Actionable Insights**: Specific remediation steps, not generic advice
- 🆓 **Completely Free**: Gemini 2.5 Flash has generous free tier limits

**See [AI_INTEGRATION.md](AI_INTEGRATION.md) for complete setup guide.**

---

## 📖 Practical Usage Guide

### Use Case 1: Basic Website Reconnaissance
Perfect for initial assessment of a target website.

```bash
# Activate virtual environment
source .venv/bin/activate

# Run standard website investigation
python3 detectivejoe.py -c website -t target-domain.com -p standard

# This will:
# ✓ Scan ports and identify services (nmap)
# ✓ Harvest emails and OSINT data (theHarvester)
# ✓ Fingerprint web technologies (whatweb)
# ✓ Analyze DNS records (dnsrecon)
# ✓ Check domain registration (whois)
# ✓ Generate AI-powered risk assessment
# ✓ Export results in TXT, HTML, JSON, CSV, XML formats
```

### Use Case 2: Deep Subdomain Enumeration
Discover all subdomains and associated infrastructure.

```bash
# Run deep scan with subdomain enumeration
python3 detectivejoe.py -c website -t target-domain.com -p deep

# This will additionally:
# ✓ Enumerate subdomains (sublist3r, dnsrecon)
# ✓ Chain discovered subdomains into additional scans
# ✓ Analyze SSL/TLS configuration (sslscan)
# ✓ Map attack surface and identify vectors
```

### Use Case 3: Security Audit with Stealth
Perform reconnaissance while minimizing detection.

```bash
# Use stealth profile with anonymity features
python3 detectivejoe.py -c website -t target-domain.com -p stealth

# Stealth features:
# ✓ TOR routing (if configured)
# ✓ Proxy rotation
# ✓ User-agent randomization
# ✓ Request delays and timing randomization
# ✓ Low aggressiveness to avoid detection
```

### Use Case 4: Organization Intelligence Gathering
Gather comprehensive information about an organization.

```bash
# Organization investigation
python3 detectivejoe.py -c organisation -t company-domain.com -p standard

# Focuses on:
# ✓ Email harvesting for employees
# ✓ Domain and subdomain enumeration
# ✓ Infrastructure mapping
# ✓ DNS records and mail servers
# ✓ Registration details
```

### Use Case 5: Quick Server Assessment
Fast assessment of a specific server or IP.

```bash
# IP/Server investigation
python3 detectivejoe.py -c ip -t 192.168.1.1 -p quick

# Analyzes:
# ✓ Open ports and running services
# ✓ SSL/TLS configuration
# ✓ Service versions and potential vulnerabilities
```

### Understanding Output

**Risk Levels:**
- `MINIMAL` (0-9): Low exposure, basic recommendations
- `LOW` (10-24): Minor issues, standard hardening needed
- `MEDIUM` (25-49): Moderate concerns, security review recommended
- `HIGH` (50-79): Significant vulnerabilities, immediate attention required
- `CRITICAL` (80-100): Severe security issues, urgent remediation needed

**Artifact Types:**
- `emails`: Email addresses discovered
- `subdomains`: Subdomain enumeration results
- `domains`: Additional domains found
- `ips`: IP addresses identified
- `ports`: Open ports detected
- `services`: Running services enumerated
- `technologies`: Web technologies fingerprinted
- `vulnerabilities`: Security issues identified

**Using Reports:**
- **TXT**: Human-readable, good for documentation
- **HTML**: Interactive, best for presentations
- **JSON**: Machine-readable, for automation/SIEM integration
- **CSV**: Spreadsheet analysis, pivot tables, filtering
- **XML**: Enterprise security tools, compliance systems

---

## ⚙️ Configuration

### Profiles System (profiles.yaml)
```yaml
profiles:
  quick:
    name: "Quick Scan"
    timeout: 60
    parallel_workers: 3
    scan_depth: 1
    aggressiveness: "low"
    enable_chaining: false
    anonymity:
      use_tor: false
      use_proxy: false
      user_agent_rotation: false
    tools:
      website: ["nmap"]
      
  standard:
    name: "Standard Scan"  
    timeout: 120
    parallel_workers: 4
    scan_depth: 2
    aggressiveness: "medium"
    enable_chaining: true
    anonymity:
      use_tor: false
      use_proxy: false
      user_agent_rotation: true
    tools:
      website: ["nmap", "theharvester"]
      organisation: ["theharvester", "nmap"]
      
  deep:
    name: "Deep Scan"
    timeout: 300
    parallel_workers: 6
    scan_depth: 3
    aggressiveness: "high"
    enable_chaining: true
    tools:
      website: ["nmap", "theharvester"]
      
  stealth:
    name: "Stealth Scan"
    timeout: 600
    parallel_workers: 2
    aggressiveness: "low"
    anonymity:
      use_tor: true
      use_proxy: true
      user_agent_rotation: true
      request_delay: 5
      randomize_timing: true
    tools:
      website: ["theharvester"]
```

### Plugin Configuration
Plugins are automatically discovered from the `plugins/` directory through YAML manifests:

**Auto-Discovery Process:**
1. Scans `plugins/` for `.yml`/`.yaml` manifest files
2. Validates manifest structure and required fields
3. Dynamically loads plugin classes from specified modules
4. Registers plugins with the global plugin registry
5. Checks tool availability and marks plugins as available/unavailable

**Plugin Chaining:**
- Artifacts discovered by plugins automatically feed into subsequent plugins
- Chain priority determines execution order
- Configurable scan depth controls chaining levels
- Aggressiveness setting limits number of chained targets

---

## 📄 Report Output

### Enhanced Report Structure with AI Analysis
```
DETECTIVE JOE v1.5 INVESTIGATION REPORT
=======================================
Investigation Type: Website Investigation
Target: example.com
Profile: standard
Date: 2025-01-15T14:30:45

EXECUTIVE SUMMARY
-----------------
Total Tasks Executed: 5
Successful Tasks: 5  
Success Rate: 100.0%
Total Execution Time: 45.23 seconds
Artifacts Found: 15
Chained Tasks: 3

ARTIFACTS DISCOVERED
--------------------
Emails: 3
Domains: 5  
IPs: 2
Open Ports: 4
Services: 3

======================================================================
AI-POWERED INTELLIGENCE ANALYSIS
======================================================================

OVERALL RISK LEVEL: HIGH (Score: 67/100)

KEY FINDINGS:
  • Discovered 12 subdomain(s)
  • Identified 8 open port(s)
  • Enumerated 5 running service(s)
  • Found 3 high/critical severity issue(s)
  • Fingerprinted 7 web technolog(ies)

IDENTIFIED VULNERABILITIES: 5
  [HIGH] Outdated SSL/TLS version: SSLv3
  [HIGH] High-risk port 3389 is exposed
  [MEDIUM] Potentially vulnerable technology detected: wordpress
  [HIGH] SSLv3 is enabled (vulnerable to POODLE)
  [MEDIUM] TLSv1.0/1.1 enabled (deprecated, should upgrade)

ATTACK SURFACE ANALYSIS:
  • Subdomains: 12
  • Open Ports: 8
  • Services: 5
  • Exposed Emails: 3

POTENTIAL ATTACK VECTORS:
  • Network service exploitation
  • SSL/TLS downgrade attacks
  • Subdomain takeover
  • Web application vulnerabilities
  • Social engineering / Phishing

MITRE ATT&CK TECHNIQUES OBSERVED:
  • T1590.001 - Gather Victim Network Information: Domain Properties
  • T1046 - Network Service Scanning
  • T1590.002 - Gather Victim Network Information: DNS

TOP RECOMMENDATIONS:
  • Upgrade SSL/TLS configuration to support only TLS 1.2+ protocols
  • Review and restrict access to high-risk ports: 3389, 445
  • Implement firewall rules and IP whitelisting for sensitive services
  • Implement security headers (CSP, HSTS, X-Frame-Options)
  • Ensure wordpress is updated to latest version
  • Regular security audits and penetration testing

======================================================================

[NMAP] - Status: COMPLETED
==================================================
Command: nmap -sV -sC -A --top-ports 1000 example.com -T4

STRUCTURED DATA:
--------------------
HOSTS: 
  - example.com (93.184.216.34)
OPEN_PORTS:
  - 80/tcp (http) - Apache httpd 2.4.41
  - 443/tcp (https) - Apache httpd 2.4.41 (SSL)

[THEHARVESTER] - Status: COMPLETED  
==================================================
Command: theHarvester -d example.com -b google,bing,duckduckgo,yahoo -l 500

STRUCTURED DATA:
--------------------
EMAILS:
  - admin@example.com
  - info@example.com
HOSTS:
  - www.example.com
  - mail.example.com

DETAILED ARTIFACTS
==================
EMAIL ARTIFACTS:
------------------------------
Value: admin@example.com
Source: theharvester
Confidence: 0.80
Tags: email, contact
Metadata: {"domain": "example.com"}

```

### Available Export Formats
Detective Joe now supports multiple export formats for integration with other tools:

1. **TXT** - Human-readable text reports with full details
2. **HTML** - Interactive HTML reports with styling and navigation
3. **JSON** - Machine-readable JSON format for automation
4. **CSV** - Spreadsheet-compatible format for analysis tools
5. **XML** - Structured XML format for enterprise security tools

All formats include:
- Complete investigation metadata
- AI-powered risk analysis and recommendations
- Vulnerability details with CVE references
- Artifact listings with confidence scores
- MITRE ATT&CK technique mappings

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd tests
python3 test_framework.py
```

Tests cover:
- Plugin base class functionality and async execution
- Plugin auto-discovery and manifest loading
- Async worker pool operations and task management
- Intelligence engine artifact processing
- Report generation in multiple formats
- State management and persistence
- Integration workflows and error handling

---

## 🛣️ v1.5 Technical Vision & Implementation Status

### 🏗️ Current Implementation Status

**✅ Core Framework (Fully Functional)**
- Async execution framework with configurable worker pools
- Plugin architecture with auto-discovery from YAML manifests
- Profile-based configuration with advanced controls
- CLI and interactive modes with comprehensive argument parsing
- Multi-format report generation (TXT/HTML/JSON/CSV/XML)
- Comprehensive test infrastructure with async support

**✅ AI-Powered Intelligence (NEW - v1.5+)**
- Automated threat assessment and risk scoring
- Vulnerability correlation and CVE mapping
- MITRE ATT&CK technique identification
- Attack surface quantification and analysis
- Context-aware security recommendations
- Smart artifact analysis and pattern recognition

**✅ Framework Components (Implemented)**
- Artifact extraction and management system
- Automatic deduplication with confidence scoring
- Advanced CVE pattern recognition and enrichment
- Persistent artifact database (JSON/binary)
- State management with save/resume/kill functionality
- Investigation persistence and recovery
- Anonymity layer with TOR/proxy/User-Agent rotation
- Plugin chaining based on artifact types

**✅ Plugin Library (8 Plugins)**
- ✅ **Nmap**: Network scanning and service detection
- ✅ **theHarvester**: Email harvesting and OSINT
- ✅ **Sublist3r**: Subdomain enumeration
- ✅ **WhatWeb**: Web technology fingerprinting
- ✅ **SSLScan**: SSL/TLS security analysis
- ✅ **DNSRecon**: DNS enumeration and zone transfers
- ✅ **WHOIS**: Domain registration information
- ✅ **Demo**: Testing mode (no external dependencies)

**⚠️ External Tool Requirements**
All plugins (except Demo) require their respective tools to be installed:
```bash
# Quick install on Kali Linux
sudo apt install nmap theharvester sublist3r whatweb sslscan dnsrecon whois
```

### Upcoming Releases

**v1.6 - Extended Plugin Library (In Progress)**
- Additional plugins: Amass, Nikto, Dirb, Masscan
- Plugin dependency management and auto-installation
- Enhanced error recovery and retry logic
- Rate limiting and advanced evasion techniques

**v1.7 - Advanced AI Features**
- Machine learning-based threat prediction
- Automated attack path analysis
- Integration with threat intelligence feeds
- Natural language report generation

**v1.8 - Enterprise Features**
- Distributed scanning across multiple nodes
- REST API for programmatic access
- Web-based dashboard and real-time monitoring
- Database storage for historical analysis

**v2.0 - Professional Platform**
- Multi-tenant support for teams/organizations
- Advanced reporting with PDF/HTML outputs
- Integration with SIEM and security platforms
- Compliance reporting and audit trails

---

## 🔧 Development & Extension

### Adding New Plugins

**1. Create Plugin YAML Manifest:**
```yaml
# plugins/mytool.yml
name: "mytool"
version: "1.0"
description: "Custom reconnaissance tool"
tool_name: "mytool"
required_tools: ["mytool"]
categories: ["website", "ip_server"]
plugin_class: "MyToolPlugin"
module_path: "mytool_plugin"
artifacts:
  produces: ["vulnerabilities", "services"]
  consumes: ["domains", "ips"]
chain_priority: 3
tags: ["security", "scanning"]
```

**2. Implement Plugin Class:**
```python
# plugins/mytool_plugin.py
from plugins.base import PluginBase

class MyToolPlugin(PluginBase):
    def __init__(self):
        super().__init__("mytool", "1.0")
    
    @property
    def tool_name(self):
        return "mytool"
    
    @property
    def categories(self):
        return ["website", "ip_server"]
    
    @property
    def required_tools(self):
        return ["mytool"]
    
    def build_command(self, target, category, **kwargs):
        return f"mytool --target {target}"
    
    def parse_output(self, output, target, category):
        return {"raw_output": output, "target": target}
```

**3. Plugin Auto-Discovery:**
Plugins are automatically discovered and loaded on framework startup.

### Profile Customization
Create custom profiles in `profiles.yaml`:
```yaml
profiles:
  my_custom:
    name: "My Custom Profile"
    description: "Tailored reconnaissance profile"
    timeout: 180
    parallel_workers: 6
    scan_depth: 2
    aggressiveness: "medium"
    enable_chaining: true
    anonymity:
      use_tor: false
      use_proxy: true
      proxy_list: ["http://proxy1:8080"]
      user_agent_rotation: true
      request_delay: 2
    tools:
      website: ["nmap", "theharvester", "mytool"]
```

### Advanced Configuration
```yaml
global_settings:
  max_parallel_workers: 8
  default_timeout: 120
  cache_enabled: true
  state_persistence: true
  intelligence_engine: true
  artifact_chaining: true
  cve_enrichment: true
  report_formats: ["txt", "html", "json"]
```

---

## 🔧 Troubleshooting

### Virtual Environment Issues
**Problem**: "Detective Joe must be run inside a virtual environment"
```bash
# Solution: Run setup script
./setup.sh

# Or manually create venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Missing Tools
**Problem**: Plugins show as "unavailable" or "No available plugins"
```bash
# Check which tools are missing
python3 detectivejoe.py --list-plugins

# Install missing tools on Kali Linux
sudo apt update
sudo apt install nmap theharvester sublist3r whatweb sslscan dnsrecon whois

# For Python-based tools
pip install theHarvester sublist3r
```

### Permission Denied
**Problem**: Cannot run nmap or other tools
```bash
# Some tools need elevated privileges
# Option 1: Run with sudo (not recommended for framework)
sudo python3 detectivejoe.py ...

# Option 2: Add capabilities to tools (better approach)
sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/nmap

# Option 3: Use demo mode for testing without privileges
python3 detectivejoe.py -c website -t example.com -p demo
```

### Import Errors
**Problem**: "Failed to import required modules"
```bash
# Ensure all framework files are present
ls -la *.py plugins/*.py

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python version (needs 3.7+)
python3 --version
```

### Timeout Issues
**Problem**: Tasks timing out before completion
```bash
# Increase timeout for slow networks
python3 detectivejoe.py -c website -t example.com --timeout 300

# Or modify profile timeout in profiles.yaml
# timeout: 300  # 5 minutes
```

### Output Directory Permissions
**Problem**: Cannot write reports
```bash
# Check/fix permissions
chmod 755 reports/
chmod 755 cache/
chmod 755 state/

# Or run from a directory where you have write access
cd ~/detective-joe-scans
python3 /path/to/detectivejoe.py ...
```

### Rate Limiting / Blocked
**Problem**: Target is rate-limiting or blocking requests
```bash
# Use stealth profile with delays
python3 detectivejoe.py -c website -t example.com -p stealth

# Or adjust aggressiveness in profiles.yaml
# aggressiveness: "low"  # Slower but more stealthy
# request_delay: 10      # 10 second delays
```

### No Results / Empty Artifacts
**Problem**: Investigation completes but finds nothing
```bash
# This can happen if:
# 1. Target has minimal exposure (good security!)
# 2. Tools didn't run successfully
# 3. Parsing failed

# Solutions:
# Check logs with verbose mode
python3 detectivejoe.py -c website -t example.com -v

# Use demo mode to verify framework works
python3 detectivejoe.py -c website -t example.com -p demo

# Test individual tools manually
nmap -sV example.com
whois example.com
```

### Getting Help
If you encounter issues not covered here:
1. Check the logs in verbose mode (`-v` flag)
2. Review generated reports for error details
3. Test tools individually outside the framework
4. Check GitHub issues: https://github.com/vinothvbt/Detective-Joe/issues
5. Ensure all dependencies are up to date

---

## ⚠️ Legal Disclaimer
This tool is intended for:
- **Educational purposes and security research**
- **Authorized penetration testing and security assessments**
- **OSINT research within legal boundaries**

**Unauthorized use against systems you do not own or have explicit permission to test is illegal** and may result in criminal charges. Users are responsible for ensuring compliance with applicable laws and regulations.

---

## 💡 Author & Credits
- **Framework Architecture**: Detective Joe v1.5 Development Team
- **Original Concept**: Detective Joe v1.0 (Kali-focused recon tool)
- **Plugin System**: Inspired by modern security framework architectures
- **Async Implementation**: Built on Python asyncio for performance

**Contributing**: We welcome contributions! Please see our contribution guidelines and submit pull requests for new plugins, features, or improvements.

---

*Detective Joe v1.5 - Where intelligence meets automation.*
