#!/usr/bin/env python3
"""
Export Utilities for Detective Joe v1.5
Export investigation results to industry-standard formats (CSV, XML).
"""

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime


class ExportManager:
    """Manager for exporting investigation results to various formats."""
    
    def __init__(self, reports_dir: Path):
        """
        Initialize export manager.
        
        Args:
            reports_dir: Directory to save exported files
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger("dj.export")
    
    def export_to_csv(self, investigation_result: Dict[str, Any], artifacts: List[Any] = None) -> str:
        """
        Export investigation results to CSV format.
        
        Args:
            investigation_result: Investigation results dictionary
            artifacts: List of artifacts
        
        Returns:
            Path to saved CSV file
        """
        target = investigation_result.get('target', 'unknown')
        category = investigation_result.get('category', 'unknown')
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Generate filename
        clean_target = "".join(c for c in target if c.isalnum() or c in ".-_")
        csv_filename = self.reports_dir / f"{clean_target}_{category}_{timestamp}.csv"
        
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Write metadata section
                writer = csv.writer(csvfile)
                writer.writerow(['# Detective Joe v1.5 Investigation Export'])
                writer.writerow(['# Target', target])
                writer.writerow(['# Category', category])
                writer.writerow(['# Date', investigation_result.get('timestamp', 'Unknown')])
                writer.writerow(['# Profile', investigation_result.get('profile', 'Unknown')])
                writer.writerow([])
                
                # Export artifacts if available
                if artifacts:
                    writer.writerow(['## ARTIFACTS'])
                    writer.writerow(['Type', 'Value', 'Source', 'Confidence', 'Tags', 'Metadata'])
                    
                    for artifact in artifacts:
                        artifact_type = artifact.type if hasattr(artifact, 'type') else 'unknown'
                        value = artifact.value if hasattr(artifact, 'value') else ''
                        source = artifact.source_plugin if hasattr(artifact, 'source_plugin') else ''
                        confidence = artifact.confidence if hasattr(artifact, 'confidence') else 0
                        tags = ', '.join(artifact.tags) if hasattr(artifact, 'tags') and artifact.tags else ''
                        metadata = str(artifact.metadata) if hasattr(artifact, 'metadata') else ''
                        
                        writer.writerow([artifact_type, value, source, confidence, tags, metadata])
                    
                    writer.writerow([])
                
                # Export vulnerabilities from AI analysis
                ai_analysis = investigation_result.get('ai_analysis')
                if ai_analysis and ai_analysis.get('vulnerabilities'):
                    writer.writerow(['## VULNERABILITIES'])
                    writer.writerow(['Severity', 'Type', 'Description', 'CVE References'])
                    
                    for vuln in ai_analysis['vulnerabilities']:
                        severity = vuln.get('severity', 'UNKNOWN')
                        vuln_type = vuln.get('type', 'Unknown')
                        description = vuln.get('description', '')
                        cves = ', '.join(vuln.get('cve_references', []))
                        
                        writer.writerow([severity, vuln_type, description, cves])
                    
                    writer.writerow([])
                
                # Export recommendations
                if ai_analysis and ai_analysis.get('recommendations'):
                    writer.writerow(['## RECOMMENDATIONS'])
                    writer.writerow(['Priority', 'Recommendation'])
                    
                    for idx, rec in enumerate(ai_analysis['recommendations'], 1):
                        writer.writerow([idx, rec])
                    
                    writer.writerow([])
                
                # Export summary statistics
                summary = investigation_result.get('summary', {})
                writer.writerow(['## SUMMARY'])
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Total Tasks', summary.get('total_tasks', 0)])
                writer.writerow(['Successful Tasks', summary.get('successful_tasks', 0)])
                writer.writerow(['Success Rate', f"{summary.get('success_rate', 0):.1f}%"])
                writer.writerow(['Execution Time', f"{summary.get('total_duration', 0):.2f}s"])
                writer.writerow(['Artifacts Found', summary.get('total_artifacts', 0)])
                
                if ai_analysis:
                    writer.writerow(['Risk Level', ai_analysis.get('risk_level', 'UNKNOWN')])
                    writer.writerow(['Risk Score', f"{ai_analysis.get('risk_score', 0)}/100"])
            
            self.logger.info(f"CSV export saved to {csv_filename}")
            return str(csv_filename)
        
        except Exception as e:
            self.logger.error(f"Failed to export to CSV: {e}")
            return None
    
    def export_to_xml(self, investigation_result: Dict[str, Any], artifacts: List[Any] = None) -> str:
        """
        Export investigation results to XML format.
        
        Args:
            investigation_result: Investigation results dictionary
            artifacts: List of artifacts
        
        Returns:
            Path to saved XML file
        """
        target = investigation_result.get('target', 'unknown')
        category = investigation_result.get('category', 'unknown')
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Generate filename
        clean_target = "".join(c for c in target if c.isalnum() or c in ".-_")
        xml_filename = self.reports_dir / f"{clean_target}_{category}_{timestamp}.xml"
        
        try:
            # Create root element
            root = ET.Element('DetectiveJoeReport', version='1.5')
            
            # Add metadata
            metadata = ET.SubElement(root, 'Metadata')
            ET.SubElement(metadata, 'Target').text = target
            ET.SubElement(metadata, 'Category').text = category
            ET.SubElement(metadata, 'InvestigationType').text = investigation_result.get('investigation_type', 'Unknown')
            ET.SubElement(metadata, 'Profile').text = investigation_result.get('profile', 'Unknown')
            ET.SubElement(metadata, 'Timestamp').text = investigation_result.get('timestamp', 'Unknown')
            
            # Add summary
            summary = investigation_result.get('summary', {})
            summary_elem = ET.SubElement(root, 'Summary')
            ET.SubElement(summary_elem, 'TotalTasks').text = str(summary.get('total_tasks', 0))
            ET.SubElement(summary_elem, 'SuccessfulTasks').text = str(summary.get('successful_tasks', 0))
            ET.SubElement(summary_elem, 'SuccessRate').text = f"{summary.get('success_rate', 0):.1f}%"
            ET.SubElement(summary_elem, 'ExecutionTime').text = f"{summary.get('total_duration', 0):.2f}s"
            ET.SubElement(summary_elem, 'ArtifactsFound').text = str(summary.get('total_artifacts', 0))
            
            # Add AI Analysis
            ai_analysis = investigation_result.get('ai_analysis')
            if ai_analysis:
                ai_elem = ET.SubElement(root, 'AIAnalysis')
                ET.SubElement(ai_elem, 'RiskLevel').text = ai_analysis.get('risk_level', 'UNKNOWN')
                ET.SubElement(ai_elem, 'RiskScore').text = str(ai_analysis.get('risk_score', 0))
                
                # Vulnerabilities
                vulns_elem = ET.SubElement(ai_elem, 'Vulnerabilities')
                for vuln in ai_analysis.get('vulnerabilities', []):
                    vuln_elem = ET.SubElement(vulns_elem, 'Vulnerability')
                    ET.SubElement(vuln_elem, 'Severity').text = vuln.get('severity', 'UNKNOWN')
                    ET.SubElement(vuln_elem, 'Type').text = vuln.get('type', 'Unknown')
                    ET.SubElement(vuln_elem, 'Description').text = vuln.get('description', '')
                    
                    cves = vuln.get('cve_references', [])
                    if cves:
                        cves_elem = ET.SubElement(vuln_elem, 'CVEReferences')
                        for cve in cves:
                            ET.SubElement(cves_elem, 'CVE').text = cve
                
                # Attack Surface
                attack_surface = ai_analysis.get('attack_surface', {})
                surface_elem = ET.SubElement(ai_elem, 'AttackSurface')
                ET.SubElement(surface_elem, 'SubdomainCount').text = str(attack_surface.get('subdomain_count', 0))
                ET.SubElement(surface_elem, 'ExposedPortCount').text = str(attack_surface.get('exposed_port_count', 0))
                ET.SubElement(surface_elem, 'ServiceCount').text = str(attack_surface.get('service_count', 0))
                ET.SubElement(surface_elem, 'EmailExposure').text = str(attack_surface.get('email_exposure', 0))
                
                # Attack Vectors
                vectors = attack_surface.get('attack_vectors', [])
                if vectors:
                    vectors_elem = ET.SubElement(surface_elem, 'AttackVectors')
                    for vector in vectors:
                        ET.SubElement(vectors_elem, 'Vector').text = vector
                
                # Recommendations
                recommendations = ai_analysis.get('recommendations', [])
                if recommendations:
                    recs_elem = ET.SubElement(ai_elem, 'Recommendations')
                    for idx, rec in enumerate(recommendations, 1):
                        rec_elem = ET.SubElement(recs_elem, 'Recommendation', priority=str(idx))
                        rec_elem.text = rec
                
                # MITRE ATT&CK
                mitre_techniques = ai_analysis.get('mitre_techniques', [])
                if mitre_techniques:
                    mitre_elem = ET.SubElement(ai_elem, 'MitreAttackTechniques')
                    for technique in mitre_techniques:
                        ET.SubElement(mitre_elem, 'Technique').text = technique
            
            # Add artifacts
            if artifacts:
                artifacts_elem = ET.SubElement(root, 'Artifacts', count=str(len(artifacts)))
                
                for artifact in artifacts:
                    artifact_elem = ET.SubElement(artifacts_elem, 'Artifact')
                    ET.SubElement(artifact_elem, 'Type').text = artifact.type if hasattr(artifact, 'type') else 'unknown'
                    ET.SubElement(artifact_elem, 'Value').text = str(artifact.value) if hasattr(artifact, 'value') else ''
                    ET.SubElement(artifact_elem, 'Source').text = artifact.source_plugin if hasattr(artifact, 'source_plugin') else ''
                    ET.SubElement(artifact_elem, 'Confidence').text = str(artifact.confidence) if hasattr(artifact, 'confidence') else '0'
                    
                    if hasattr(artifact, 'tags') and artifact.tags:
                        tags_elem = ET.SubElement(artifact_elem, 'Tags')
                        for tag in artifact.tags:
                            ET.SubElement(tags_elem, 'Tag').text = tag
            
            # Add plugin results
            plugin_results = investigation_result.get('plugin_results', {})
            if plugin_results:
                results_elem = ET.SubElement(root, 'PluginResults', count=str(len(plugin_results)))
                
                for task_id, result in plugin_results.items():
                    result_elem = ET.SubElement(results_elem, 'PluginResult', id=task_id)
                    ET.SubElement(result_elem, 'Plugin').text = result.get('plugin', 'Unknown')
                    ET.SubElement(result_elem, 'Status').text = result.get('status', 'Unknown')
                    ET.SubElement(result_elem, 'Duration').text = f"{result.get('duration', 0):.2f}s"
                    
                    if result.get('error'):
                        ET.SubElement(result_elem, 'Error').text = result['error']
            
            # Pretty print XML
            try:
                xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            except Exception as e:
                self.logger.warning(f"Failed to pretty print XML, using basic format: {e}")
                xml_string = ET.tostring(root, encoding='unicode')
            
            # Write to file
            with open(xml_filename, 'w', encoding='utf-8') as f:
                f.write(xml_string)
            
            self.logger.info(f"XML export saved to {xml_filename}")
            return str(xml_filename)
        
        except Exception as e:
            self.logger.error(f"Failed to export to XML: {e}")
            return None
    
    def export_all_formats(self, investigation_result: Dict[str, Any], artifacts: List[Any] = None) -> Dict[str, str]:
        """
        Export investigation results to all available formats.
        
        Args:
            investigation_result: Investigation results dictionary
            artifacts: List of artifacts
        
        Returns:
            Dictionary mapping format names to file paths
        """
        exports = {}
        
        csv_file = self.export_to_csv(investigation_result, artifacts)
        if csv_file:
            exports['csv'] = csv_file
        
        xml_file = self.export_to_xml(investigation_result, artifacts)
        if xml_file:
            exports['xml'] = xml_file
        
        return exports
