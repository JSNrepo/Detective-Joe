#!/usr/bin/env python3
"""
Gemini AI Service for Detective Joe
Handles all interactions with Google Gemini 2.5 Flash API for intelligent reconnaissance analysis.
Uses the new google-genai SDK for Gemini 2.5 Flash support.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional


class GeminiService:
    """
    Service class for interacting with Google Gemini 2.5 Flash API.
    Provides intelligent analysis of reconnaissance data.
    Uses the new google-genai SDK (not google-generativeai).
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini AI service.
        
        Args:
            api_key: Google API key for Gemini. If None, tries to read from env.
        """
        self.logger = logging.getLogger("dj.gemini")
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        self.enabled = False
        
        # Try to initialize Gemini
        self._initialize_gemini()
    
    def _initialize_gemini(self) -> None:
        """Initialize Gemini AI client with new google-genai SDK."""
        try:
            from google import genai
            
            if not self.api_key:
                self.logger.warning("No Gemini API key found. AI features will use fallback analysis.")
                self.logger.info("Set GEMINI_API_KEY environment variable to enable Gemini AI features.")
                return
            
            # Initialize the new Gemini client
            # The client automatically picks up the API key from the environment variable
            os.environ['GEMINI_API_KEY'] = self.api_key
            self.client = genai.Client()
            
            self.enabled = True
            self.logger.info("Gemini 2.5 Flash AI initialized successfully")
            
        except ImportError:
            self.logger.warning("google-genai package not installed. Run: pip install google-genai")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Gemini AI: {e}")
    
    def is_enabled(self) -> bool:
        """Check if Gemini AI is enabled and ready."""
        return self.enabled and self.client is not None
    
    def analyze_recon_data(self, artifacts: List[Dict[str, Any]], 
                          plugin_results: List[Dict[str, Any]],
                          target: str) -> Dict[str, Any]:
        """
        Analyze reconnaissance data using Gemini AI.
        
        Args:
            artifacts: List of discovered artifacts
            plugin_results: Raw plugin execution results
            target: Investigation target
            
        Returns:
            AI-generated analysis report
        """
        if not self.is_enabled():
            return self._fallback_analysis(artifacts, plugin_results, target)
        
        try:
            # Prepare data summary for AI analysis
            data_summary = self._prepare_data_summary(artifacts, plugin_results, target)
            
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(data_summary, target)
            
            # Get AI analysis using new SDK
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            # Parse and structure the response
            analysis = self._parse_ai_response(response.text)
            
            self.logger.info(f"Gemini AI analysis completed for target: {target}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Gemini AI analysis failed: {e}")
            return self._fallback_analysis(artifacts, plugin_results, target)
    
    def _prepare_data_summary(self, artifacts: List[Dict[str, Any]], 
                             plugin_results: List[Dict[str, Any]],
                             target: str) -> Dict[str, Any]:
        """Prepare a concise summary of reconnaissance data for AI analysis."""
        summary = {
            "target": target,
            "total_artifacts": len(artifacts),
            "artifacts_by_type": {},
            "plugins_executed": [],
            "key_findings": []
        }
        
        # Summarize artifacts by type
        for artifact in artifacts:
            artifact_type = artifact.get("type", "unknown")
            if artifact_type not in summary["artifacts_by_type"]:
                summary["artifacts_by_type"][artifact_type] = []
            
            # Add value (limit to reasonable size)
            if len(summary["artifacts_by_type"][artifact_type]) < 50:
                summary["artifacts_by_type"][artifact_type].append(artifact.get("value", ""))
        
        # Summarize plugin results
        for result in plugin_results:
            if result.get("status") == "completed":
                plugin_name = result.get("plugin", "unknown")
                summary["plugins_executed"].append(plugin_name)
                
                # Extract key data from parsed results
                parsed_data = result.get("result", {}).get("parsed_data", {})
                if parsed_data:
                    summary["key_findings"].append({
                        "plugin": plugin_name,
                        "data": self._extract_key_points(parsed_data)
                    })
        
        return summary
    
    def _extract_key_points(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key points from parsed plugin data."""
        key_points = {}
        
        # Extract important fields
        important_fields = ["open_ports", "services", "vulnerabilities", "emails", 
                          "domains", "hosts", "ips", "technologies", "ssl_versions"]
        
        for field in important_fields:
            if field in parsed_data and parsed_data[field]:
                # Limit list sizes for AI processing
                value = parsed_data[field]
                if isinstance(value, list) and len(value) > 20:
                    key_points[field] = value[:20] + [f"... and {len(value) - 20} more"]
                else:
                    key_points[field] = value
        
        return key_points
    
    def _create_analysis_prompt(self, data_summary: Dict[str, Any], target: str) -> str:
        """Create a detailed prompt for Gemini AI analysis."""
        prompt = f"""You are a cybersecurity expert analyzing reconnaissance data for target: {target}

RECONNAISSANCE DATA SUMMARY:
{json.dumps(data_summary, indent=2)}

Please provide a comprehensive security analysis including:

1. RISK ASSESSMENT:
   - Overall risk level (MINIMAL, LOW, MEDIUM, HIGH, CRITICAL)
   - Risk score (0-100)
   - Brief justification

2. KEY FINDINGS:
   - List the most important discoveries
   - Highlight any sensitive information exposed
   - Identify patterns or anomalies

3. VULNERABILITIES:
   - Identify specific security vulnerabilities
   - Classify by severity (HIGH, MEDIUM, LOW)
   - Provide CVE references if applicable

4. ATTACK SURFACE:
   - Quantify exposed services and ports
   - Assess subdomain exposure
   - Evaluate technology stack risks

5. SECURITY RECOMMENDATIONS:
   - Provide actionable security recommendations
   - Prioritize by impact and urgency
   - Include specific remediation steps

6. ATTACK VECTORS:
   - List potential attack vectors based on findings
   - Describe exploitation scenarios

Format your response as a structured JSON with these sections:
{{
  "risk_score": <number 0-100>,
  "risk_level": "<MINIMAL|LOW|MEDIUM|HIGH|CRITICAL>",
  "key_findings": ["finding1", "finding2", ...],
  "vulnerabilities": [
    {{
      "type": "type",
      "severity": "HIGH|MEDIUM|LOW",
      "description": "description",
      "recommendation": "how to fix"
    }}
  ],
  "attack_surface": {{
    "subdomain_count": <number>,
    "exposed_port_count": <number>,
    "service_count": <number>,
    "email_exposure": <number>
  }},
  "recommendations": ["rec1", "rec2", ...],
  "attack_vectors": ["vector1", "vector2", ...],
  "executive_summary": "A brief 2-3 sentence summary of the overall security posture"
}}

Provide ONLY valid JSON, no markdown formatting or additional text."""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate AI response."""
        try:
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["risk_score", "risk_level", "key_findings", 
                             "vulnerabilities", "recommendations"]
            for field in required_fields:
                if field not in analysis:
                    self.logger.warning(f"Missing field in AI response: {field}")
                    analysis[field] = [] if field != "risk_score" else 0
            
            return analysis
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AI response as JSON: {e}")
            self.logger.debug(f"Response text: {response_text[:500]}")
            
            # Return basic structure
            return {
                "risk_score": 50,
                "risk_level": "MEDIUM",
                "key_findings": ["AI analysis parsing failed"],
                "vulnerabilities": [],
                "recommendations": ["Review findings manually"],
                "executive_summary": "Automated AI analysis encountered parsing issues. Manual review recommended."
            }
    
    def _fallback_analysis(self, artifacts: List[Dict[str, Any]], 
                          plugin_results: List[Dict[str, Any]],
                          target: str) -> Dict[str, Any]:
        """
        Fallback analysis when Gemini AI is not available.
        Provides basic rule-based analysis.
        """
        self.logger.info("Using fallback analysis (Gemini AI not available)")
        
        # Basic analysis based on artifact counts
        artifact_types = {}
        for artifact in artifacts:
            artifact_type = artifact.get("type", "unknown")
            artifact_types[artifact_type] = artifact_types.get(artifact_type, 0) + 1
        
        # Calculate basic risk score using weighted factors
        # Risk score weights: higher values indicate more significant findings
        RISK_WEIGHT_PORT = 2        # Each open port adds 2 points
        RISK_WEIGHT_SERVICE = 3     # Each service adds 3 points  
        RISK_WEIGHT_SUBDOMAIN = 1   # Each subdomain adds 1 point
        RISK_WEIGHT_EMAIL = 1       # Each exposed email adds 1 point
        MAX_RISK_SCORE = 100        # Cap risk score at 100
        
        risk_score = 0
        risk_score += artifact_types.get("port", 0) * RISK_WEIGHT_PORT
        risk_score += artifact_types.get("service", 0) * RISK_WEIGHT_SERVICE
        risk_score += artifact_types.get("subdomain", 0) * RISK_WEIGHT_SUBDOMAIN
        risk_score += artifact_types.get("email", 0) * RISK_WEIGHT_EMAIL
        risk_score = min(risk_score, MAX_RISK_SCORE)
        
        # Determine risk level based on score
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 25:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "key_findings": [
                f"Discovered {len(artifacts)} total artifacts",
                f"Analyzed target: {target}",
                "Basic rule-based analysis completed"
            ],
            "vulnerabilities": [],
            "attack_surface": {
                "subdomain_count": artifact_types.get("subdomain", 0),
                "exposed_port_count": artifact_types.get("port", 0),
                "service_count": artifact_types.get("service", 0),
                "email_exposure": artifact_types.get("email", 0)
            },
            "recommendations": [
                "Install Gemini AI for detailed analysis (set GEMINI_API_KEY)",
                "Review all discovered artifacts manually",
                "Verify security configurations"
            ],
            "attack_vectors": [
                "Manual security review required"
            ],
            "executive_summary": f"Basic analysis completed for {target}. {len(artifacts)} artifacts discovered. Enable Gemini AI for detailed security insights.",
            "ai_enabled": False
        }
    
    def generate_human_readable_summary(self, analysis: Dict[str, Any], target: str) -> str:
        """
        Generate a human-readable summary from AI analysis.
        
        Args:
            analysis: AI analysis results
            target: Investigation target
            
        Returns:
            Formatted text summary
        """
        if self.is_enabled():
            prompt = f"""Create a brief, professional security summary for this reconnaissance report:

Target: {target}
Risk Level: {analysis.get('risk_level', 'UNKNOWN')}
Risk Score: {analysis.get('risk_score', 0)}/100

Key Findings:
{chr(10).join('- ' + f for f in analysis.get('key_findings', [])[:5])}

Please provide a 3-4 sentence executive summary that a security manager would understand."""
            
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                self.logger.error(f"Failed to generate summary: {e}")
        
        # Fallback summary
        summary = f"""RECONNAISSANCE SUMMARY FOR {target.upper()}

Risk Assessment: {analysis.get('risk_level', 'UNKNOWN')} ({analysis.get('risk_score', 0)}/100)

The reconnaissance scan discovered {len(analysis.get('key_findings', []))} key findings. """
        
        if analysis.get('vulnerabilities'):
            summary += f"{len(analysis.get('vulnerabilities', []))} potential vulnerabilities were identified. "
        
        if analysis.get('recommendations'):
            summary += f"Review the {len(analysis.get('recommendations', []))} security recommendations provided."
        
        return summary
