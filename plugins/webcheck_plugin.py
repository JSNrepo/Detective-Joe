#!/usr/bin/env python3
"""
Web-Check Plugin for Detective Joe v1.5
Provides direct Web-Check OSINT integration links for website investigations.
"""

import json
import os
import re
import shlex
from typing import Dict, Any, List
from urllib.parse import quote
from .base import PluginBase


class WebCheckPlugin(PluginBase):
    """Plugin for Web-Check integration."""

    def __init__(self):
        super().__init__("webcheck", "1.0")

    @property
    def tool_name(self) -> str:
        return "web-check-free"

    @property
    def categories(self) -> List[str]:
        return ["website"]

    @property
    def required_tools(self) -> List[str]:
        return ["python3"]

    def build_command(self, target: str, category: str, **kwargs) -> str:
        """
        Build command that emits structured Web-Check integration data.
        """
        base_url = os.environ.get("WEB_CHECK_BASE_URL", "https://web-check.xyz").strip().rstrip("/")
        if not base_url:
            base_url = "https://web-check.xyz"

        normalized_target = target.strip()
        if not normalized_target.startswith(("http://", "https://")):
            normalized_target = f"https://{normalized_target}"

        assessment_url = f"{base_url}/?url={quote(normalized_target, safe='')}"
        payload = {
            "target": normalized_target,
            "webcheck_instance": base_url,
            "assessment_url": assessment_url,
            "status": "ready",
            "notes": [
                "Open the assessment URL to run full Web-Check OSINT analysis.",
                "Set WEB_CHECK_BASE_URL to your self-hosted web-check-free instance if needed."
            ]
        }

        code = f"import json; print(json.dumps({payload!r}))"
        return f"python3 -c {shlex.quote(code)}"

    def parse_output(self, output: str, target: str, category: str) -> Dict[str, Any]:
        """
        Parse emitted JSON output.
        """
        if not output or not output.strip():
            return {
                "target": target,
                "category": category,
                "status": "error",
                "reason": "No output received from webcheck plugin"
            }

        try:
            parsed = json.loads(output.strip().splitlines()[-1])
            parsed["category"] = category
            return parsed
        except json.JSONDecodeError:
            return {
                "target": target,
                "category": category,
                "status": "error",
                "reason": "Failed to parse webcheck output",
                "raw_output": output
            }

    def validate_target(self, target: str, category: str) -> bool:
        """Validate website target for Web-Check links."""
        if not target or not target.strip():
            return False
        if " " in target.strip():
            return False

        normalized = target.strip()
        if normalized.startswith(("http://", "https://")):
            normalized = normalized.split("://", 1)[1]
        normalized = normalized.split("/", 1)[0]

        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return re.match(domain_pattern, normalized) is not None

