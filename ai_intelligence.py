#!/usr/bin/env python3
"""
AI-Powered Intelligence Analyzer for Detective Joe v1.5
Advanced analysis and correlation of reconnaissance data using AI techniques.
"""

import re
import json
from typing import Dict, Any, List, Set, Tuple
from collections import defaultdict
import logging


class AIIntelligenceAnalyzer:
    """
    AI-powered intelligence analyzer for reconnaissance data.
    Provides automated threat assessment, vulnerability correlation, and actionable recommendations.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("dj.ai_analyzer")
        
        # Known vulnerability patterns and indicators
        self.vulnerability_patterns = {
            "outdated_ssl": ["sslv2", "sslv3", "tlsv1.0", "tlsv1.1"],
            "weak_ciphers": ["rc4", "des", "3des", "md5", "sha1"],
            "security_headers": ["x-frame-options", "content-security-policy", "strict-transport-security"],
            "sensitive_info": ["debug", "test", "admin", "backup", "config", "api_key", "password"],
            "open_ports_high_risk": [21, 23, 445, 3389, 5900],
            "web_technologies": ["wordpress", "joomla", "drupal", "struts", "spring"]
        }
        
        # MITRE ATT&CK mapping for reconnaissance techniques
        self.mitre_mapping = {
            "subdomain_enum": "T1590.001 - Gather Victim Network Information: Domain Properties",
            "port_scanning": "T1046 - Network Service Scanning",
            "dns_enum": "T1590.002 - Gather Victim Network Information: DNS",
            "ssl_analysis": "T1590.001 - Gather Victim Network Information: Domain Properties",
            "whois_lookup": "T1590.001 - Gather Victim Network Information: Domain Properties",
            "tech_fingerprint": "T1592.002 - Gather Victim Host Information: Software"
        }
    
    def analyze_reconnaissance_results(self, artifacts: List[Dict[str, Any]], 
                                     plugin_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive AI-powered analysis of reconnaissance results.
        
        Args:
            artifacts: List of extracted artifacts from intelligence engine
            plugin_results: Raw results from all executed plugins
        
        Returns:
            Analysis report with risk assessment and recommendations
        """
        analysis = {
            "risk_score": 0,
            "risk_level": "unknown",
            "vulnerabilities": [],
            "security_concerns": [],
            "exposed_services": [],
            "attack_surface": {},
            "recommendations": [],
            "mitre_techniques": [],
            "key_findings": []
        }
        
        # Analyze artifacts
        artifact_analysis = self._analyze_artifacts(artifacts)
        
        # Analyze plugin results
        plugin_analysis = self._analyze_plugin_results(plugin_results)
        
        # Vulnerability correlation
        vulnerabilities = self._correlate_vulnerabilities(artifact_analysis, plugin_analysis)
        
        # Risk assessment
        risk_assessment = self._calculate_risk_score(vulnerabilities, artifact_analysis, plugin_analysis)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities, artifact_analysis, plugin_analysis)
        
        # Attack surface analysis
        attack_surface = self._analyze_attack_surface(artifact_analysis, plugin_analysis)
        
        # Compile final analysis
        analysis.update({
            "risk_score": risk_assessment["score"],
            "risk_level": risk_assessment["level"],
            "vulnerabilities": vulnerabilities,
            "security_concerns": artifact_analysis.get("concerns", []),
            "exposed_services": plugin_analysis.get("services", []),
            "attack_surface": attack_surface,
            "recommendations": recommendations,
            "mitre_techniques": self._identify_mitre_techniques(plugin_results),
            "key_findings": self._extract_key_findings(artifact_analysis, plugin_analysis, vulnerabilities)
        })
        
        return analysis
    
    def _analyze_artifacts(self, artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze artifacts for patterns and security concerns."""
        analysis = {
            "subdomains": [],
            "emails": [],
            "open_ports": [],
            "technologies": [],
            "concerns": [],
            "domain_info": {}
        }
        
        for artifact in artifacts:
            artifact_type = artifact.get("type", "")
            value = artifact.get("value", "")
            
            if artifact_type == "subdomain":
                analysis["subdomains"].append(value)
                # Check for sensitive subdomain names
                if any(sensitive in value.lower() for sensitive in self.vulnerability_patterns["sensitive_info"]):
                    analysis["concerns"].append(f"Potentially sensitive subdomain found: {value}")
            
            elif artifact_type == "email":
                analysis["emails"].append(value)
            
            elif artifact_type == "port":
                port_num = int(value) if str(value).isdigit() else 0
                analysis["open_ports"].append(port_num)
                if port_num in self.vulnerability_patterns["open_ports_high_risk"]:
                    analysis["concerns"].append(f"High-risk port {port_num} is open")
            
            elif artifact_type == "technology":
                analysis["technologies"].append(value)
        
        return analysis
    
    def _analyze_plugin_results(self, plugin_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze raw plugin results for security indicators."""
        analysis = {
            "services": [],
            "ssl_issues": [],
            "web_tech": [],
            "dns_records": []
        }
        
        for result in plugin_results:
            plugin_name = result.get("plugin", "")
            parsed_data = result.get("parsed_data", {})
            
            if plugin_name == "sslscan":
                # Analyze SSL/TLS configuration
                supported_versions = parsed_data.get("ssl_versions_supported", [])
                for version in supported_versions:
                    if any(weak in version.lower() for weak in self.vulnerability_patterns["outdated_ssl"]):
                        analysis["ssl_issues"].append(f"Outdated SSL/TLS version: {version}")
            
            elif plugin_name == "nmap":
                # Analyze open ports and services
                open_ports = parsed_data.get("OPEN_PORTS", [])
                for port_info in open_ports:
                    if isinstance(port_info, dict):
                        analysis["services"].append(port_info)
            
            elif plugin_name == "whatweb":
                # Analyze web technologies
                technologies = parsed_data.get("technologies", [])
                analysis["web_tech"].extend(technologies)
            
            elif plugin_name == "dnsrecon":
                # Analyze DNS records
                dns_records = parsed_data.get("dns_records", {})
                analysis["dns_records"].append(dns_records)
        
        return analysis
    
    def _correlate_vulnerabilities(self, artifact_analysis: Dict[str, Any], 
                                   plugin_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Correlate findings to identify specific vulnerabilities."""
        vulnerabilities = []
        
        # SSL/TLS vulnerabilities
        for issue in plugin_analysis.get("ssl_issues", []):
            vulnerabilities.append({
                "type": "SSL/TLS Configuration",
                "severity": "HIGH",
                "description": issue,
                "cve_references": self._get_ssl_cves(issue)
            })
        
        # High-risk port exposure
        for port in artifact_analysis.get("open_ports", []):
            if port in self.vulnerability_patterns["open_ports_high_risk"]:
                vulnerabilities.append({
                    "type": "Exposed Service",
                    "severity": "HIGH" if port in [23, 445, 3389] else "MEDIUM",
                    "description": f"High-risk port {port} is exposed",
                    "port": port
                })
        
        # Vulnerable web technologies
        for tech in plugin_analysis.get("web_tech", []):
            tech_name = tech.get("name", "").lower() if isinstance(tech, dict) else str(tech).lower()
            for vuln_tech in self.vulnerability_patterns["web_technologies"]:
                if vuln_tech in tech_name:
                    vulnerabilities.append({
                        "type": "Vulnerable Technology",
                        "severity": "MEDIUM",
                        "description": f"Potentially vulnerable technology detected: {tech_name}",
                        "recommendation": f"Ensure {tech_name} is updated to latest version"
                    })
        
        return vulnerabilities
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict[str, Any]], 
                             artifact_analysis: Dict[str, Any],
                             plugin_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score based on findings."""
        score = 0
        
        # Vulnerability scoring
        severity_weights = {"CRITICAL": 25, "HIGH": 15, "MEDIUM": 8, "LOW": 3}
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "LOW")
            score += severity_weights.get(severity, 0)
        
        # Attack surface scoring
        score += len(artifact_analysis.get("open_ports", [])) * 2
        score += len(artifact_analysis.get("subdomains", [])) * 1
        score += len(plugin_analysis.get("services", [])) * 3
        
        # Security concerns
        score += len(artifact_analysis.get("concerns", [])) * 5
        score += len(plugin_analysis.get("ssl_issues", [])) * 10
        
        # Determine risk level
        if score >= 80:
            level = "CRITICAL"
        elif score >= 50:
            level = "HIGH"
        elif score >= 25:
            level = "MEDIUM"
        elif score >= 10:
            level = "LOW"
        else:
            level = "MINIMAL"
        
        return {
            "score": min(score, 100),  # Cap at 100
            "level": level
        }
    
    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]], 
                                 artifact_analysis: Dict[str, Any],
                                 plugin_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable security recommendations."""
        recommendations = []
        
        # SSL/TLS recommendations
        if plugin_analysis.get("ssl_issues"):
            recommendations.append("Upgrade SSL/TLS configuration to support only TLS 1.2+ protocols")
            recommendations.append("Disable weak cipher suites and enable forward secrecy")
        
        # Port exposure recommendations
        high_risk_ports = [p for p in artifact_analysis.get("open_ports", []) 
                          if p in self.vulnerability_patterns["open_ports_high_risk"]]
        if high_risk_ports:
            recommendations.append(f"Review and restrict access to high-risk ports: {', '.join(map(str, high_risk_ports))}")
            recommendations.append("Implement firewall rules and IP whitelisting for sensitive services")
        
        # Subdomain recommendations
        if len(artifact_analysis.get("subdomains", [])) > 10:
            recommendations.append("Large attack surface detected - Review and consolidate subdomains")
            recommendations.append("Ensure all subdomains have proper security configurations")
        
        # General recommendations
        recommendations.append("Implement security headers (CSP, HSTS, X-Frame-Options)")
        recommendations.append("Regular security audits and penetration testing")
        recommendations.append("Monitor for new vulnerabilities in identified technologies")
        
        # Vulnerability-specific recommendations
        for vuln in vulnerabilities:
            if "recommendation" in vuln:
                recommendations.append(vuln["recommendation"])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _analyze_attack_surface(self, artifact_analysis: Dict[str, Any],
                               plugin_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and quantify the attack surface."""
        return {
            "subdomain_count": len(artifact_analysis.get("subdomains", [])),
            "exposed_port_count": len(artifact_analysis.get("open_ports", [])),
            "service_count": len(plugin_analysis.get("services", [])),
            "email_exposure": len(artifact_analysis.get("emails", [])),
            "technology_stack_size": len(plugin_analysis.get("web_tech", [])),
            "attack_vectors": self._identify_attack_vectors(artifact_analysis, plugin_analysis)
        }
    
    def _identify_attack_vectors(self, artifact_analysis: Dict[str, Any],
                                plugin_analysis: Dict[str, Any]) -> List[str]:
        """Identify potential attack vectors."""
        vectors = []
        
        if artifact_analysis.get("open_ports"):
            vectors.append("Network service exploitation")
        
        if plugin_analysis.get("ssl_issues"):
            vectors.append("SSL/TLS downgrade attacks")
        
        if artifact_analysis.get("subdomains"):
            vectors.append("Subdomain takeover")
        
        if plugin_analysis.get("web_tech"):
            vectors.append("Web application vulnerabilities")
        
        if artifact_analysis.get("emails"):
            vectors.append("Social engineering / Phishing")
        
        return vectors
    
    def _identify_mitre_techniques(self, plugin_results: List[Dict[str, Any]]) -> List[str]:
        """Map executed plugins to MITRE ATT&CK techniques."""
        techniques = []
        
        for result in plugin_results:
            plugin_name = result.get("plugin", "").lower()
            
            if "sublist3r" in plugin_name:
                techniques.append(self.mitre_mapping["subdomain_enum"])
            elif "nmap" in plugin_name:
                techniques.append(self.mitre_mapping["port_scanning"])
            elif "dnsrecon" in plugin_name:
                techniques.append(self.mitre_mapping["dns_enum"])
            elif "sslscan" in plugin_name:
                techniques.append(self.mitre_mapping["ssl_analysis"])
            elif "whois" in plugin_name:
                techniques.append(self.mitre_mapping["whois_lookup"])
            elif "whatweb" in plugin_name:
                techniques.append(self.mitre_mapping["tech_fingerprint"])
        
        return list(set(techniques))  # Remove duplicates
    
    def _extract_key_findings(self, artifact_analysis: Dict[str, Any],
                            plugin_analysis: Dict[str, Any],
                            vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Extract and summarize key findings."""
        findings = []
        
        # Subdomain findings
        subdomain_count = len(artifact_analysis.get("subdomains", []))
        if subdomain_count > 0:
            findings.append(f"Discovered {subdomain_count} subdomain(s)")
        
        # Port findings
        port_count = len(artifact_analysis.get("open_ports", []))
        if port_count > 0:
            findings.append(f"Identified {port_count} open port(s)")
        
        # Service findings
        service_count = len(plugin_analysis.get("services", []))
        if service_count > 0:
            findings.append(f"Enumerated {service_count} running service(s)")
        
        # Vulnerability findings
        high_severity_vulns = [v for v in vulnerabilities if v.get("severity") in ["HIGH", "CRITICAL"]]
        if high_severity_vulns:
            findings.append(f"Found {len(high_severity_vulns)} high/critical severity issue(s)")
        
        # Technology findings
        tech_count = len(plugin_analysis.get("web_tech", []))
        if tech_count > 0:
            findings.append(f"Fingerprinted {tech_count} web technolog(ies)")
        
        return findings
    
    def _get_ssl_cves(self, issue: str) -> List[str]:
        """Map SSL/TLS issues to known CVEs."""
        cve_mapping = {
            "sslv2": ["CVE-2016-0800 (DROWN)"],
            "sslv3": ["CVE-2014-3566 (POODLE)"],
            "tlsv1.0": ["CVE-2011-3389 (BEAST)"],
            "rc4": ["CVE-2013-2566", "CVE-2015-2808"]
        }
        
        cves = []
        issue_lower = issue.lower()
        for key, value in cve_mapping.items():
            if key in issue_lower:
                cves.extend(value)
        
        return cves
    
    def generate_executive_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable executive summary."""
        summary_lines = []
        
        summary_lines.append("=" * 70)
        summary_lines.append("AI-POWERED INTELLIGENCE ANALYSIS")
        summary_lines.append("=" * 70)
        summary_lines.append("")
        
        # Risk assessment
        risk_level = analysis.get("risk_level", "UNKNOWN")
        risk_score = analysis.get("risk_score", 0)
        summary_lines.append(f"OVERALL RISK LEVEL: {risk_level} (Score: {risk_score}/100)")
        summary_lines.append("")
        
        # Key findings
        key_findings = analysis.get("key_findings", [])
        if key_findings:
            summary_lines.append("KEY FINDINGS:")
            for finding in key_findings:
                summary_lines.append(f"  • {finding}")
            summary_lines.append("")
        
        # Vulnerabilities
        vulnerabilities = analysis.get("vulnerabilities", [])
        if vulnerabilities:
            summary_lines.append(f"IDENTIFIED VULNERABILITIES: {len(vulnerabilities)}")
            for vuln in vulnerabilities[:5]:  # Show top 5
                severity = vuln.get("severity", "UNKNOWN")
                description = vuln.get("description", "No description")
                summary_lines.append(f"  [{severity}] {description}")
            if len(vulnerabilities) > 5:
                summary_lines.append(f"  ... and {len(vulnerabilities) - 5} more")
            summary_lines.append("")
        
        # Attack surface
        attack_surface = analysis.get("attack_surface", {})
        summary_lines.append("ATTACK SURFACE ANALYSIS:")
        summary_lines.append(f"  • Subdomains: {attack_surface.get('subdomain_count', 0)}")
        summary_lines.append(f"  • Open Ports: {attack_surface.get('exposed_port_count', 0)}")
        summary_lines.append(f"  • Services: {attack_surface.get('service_count', 0)}")
        summary_lines.append(f"  • Exposed Emails: {attack_surface.get('email_exposure', 0)}")
        summary_lines.append("")
        
        # Attack vectors
        attack_vectors = attack_surface.get("attack_vectors", [])
        if attack_vectors:
            summary_lines.append("POTENTIAL ATTACK VECTORS:")
            for vector in attack_vectors:
                summary_lines.append(f"  • {vector}")
            summary_lines.append("")
        
        # MITRE ATT&CK
        mitre_techniques = analysis.get("mitre_techniques", [])
        if mitre_techniques:
            summary_lines.append("MITRE ATT&CK TECHNIQUES OBSERVED:")
            for technique in mitre_techniques[:3]:  # Show top 3
                summary_lines.append(f"  • {technique}")
            summary_lines.append("")
        
        # Recommendations
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            summary_lines.append("TOP RECOMMENDATIONS:")
            for rec in recommendations[:5]:  # Show top 5
                summary_lines.append(f"  • {rec}")
            summary_lines.append("")
        
        summary_lines.append("=" * 70)
        
        return "\n".join(summary_lines)
