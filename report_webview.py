#!/usr/bin/env python3
"""
Detective Joe v1.5 - Webview Dashboard
Serve generated reports with a clean browser UI.
"""

import json
import logging
import heapq
import os
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import quote


DEFAULT_WEB_CHECK_URL = "https://web-check.xyz"


class ReportWebView:
    """Simple HTTP dashboard for browsing report files."""
    MAX_INDEX_REPORTS = 200

    def __init__(self, reports_dir: Path, web_check_base_url: str = None):
        self.reports_dir = Path(reports_dir)
        base_url = web_check_base_url or os.environ.get("WEB_CHECK_BASE_URL", DEFAULT_WEB_CHECK_URL)
        self.web_check_base_url = base_url.rstrip("/")
        self.logger = logging.getLogger("dj.webview")

    def _load_report_index(self) -> List[Dict[str, Any]]:
        """Load report metadata from JSON exports."""
        reports = []
        json_reports = heapq.nlargest(
            self.MAX_INDEX_REPORTS,
            self.reports_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime
        )

        for json_file in json_reports:
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                investigation = data.get("investigation", {})
                summary = data.get("summary", {})

                target = str(investigation.get("target", "unknown"))
                stem = json_file.stem

                file_links = {}
                for ext in ["html", "json", "txt", "csv", "xml"]:
                    report_file = self.reports_dir / f"{stem}.{ext}"
                    if report_file.exists():
                        file_links[ext] = report_file.name

                reports.append({
                    "target": target,
                    "type": investigation.get("type", "Unknown"),
                    "category": investigation.get("category", "Unknown"),
                    "profile": investigation.get("profile", "Unknown"),
                    "timestamp": investigation.get("timestamp", "Unknown"),
                    "tasks": summary.get("total_tasks", 0),
                    "success_rate": summary.get("success_rate", 0),
                    "artifacts": summary.get("total_artifacts", 0),
                    "links": file_links,
                    "webcheck_url": f"{self.web_check_base_url}/?url={quote(target, safe='')}"
                })
            except Exception as e:
                self.logger.warning(f"Skipping unreadable JSON report {json_file.name}: {e}")

        return reports

    def _render_dashboard_html(self) -> str:
        """Render dashboard HTML."""
        reports = self._load_report_index()
        rows = []

        for report in reports:
            link_parts = []
            for ext in ["html", "json", "txt", "csv", "xml"]:
                if ext in report["links"]:
                    filename = escape(report["links"][ext])
                    link_parts.append(f'<a href="/{filename}" target="_blank">{ext.upper()}</a>')

            link_parts.append(f'<a href="{escape(report["webcheck_url"])}" target="_blank">WEB-CHECK</a>')
            links_html = " | ".join(link_parts)

            rows.append(
                "<tr>"
                f"<td>{escape(report['timestamp'])}</td>"
                f"<td>{escape(report['target'])}</td>"
                f"<td>{escape(report['category'])}</td>"
                f"<td>{escape(report['profile'])}</td>"
                f"<td>{report['tasks']}</td>"
                f"<td>{float(report['success_rate']):.1f}%</td>"
                f"<td>{report['artifacts']}</td>"
                f"<td>{links_html}</td>"
                "</tr>"
            )

        table_rows = "\n".join(rows) if rows else (
            "<tr><td colspan='8'>No JSON reports found yet. Run an investigation first.</td></tr>"
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Detective Joe Webview</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f5f7fb;
      color: #1f2937;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: #fff;
      border-radius: 10px;
      padding: 24px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }}
    h1 {{
      margin-top: 0;
    }}
    .hint {{
      color: #4b5563;
      margin-bottom: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border: 1px solid #e5e7eb;
      padding: 10px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #eef2ff;
    }}
    a {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🔍 Detective Joe Webview</h1>
    <p class="hint">Interactive report index with direct links to local report files and Web-Check.</p>
    <table>
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Target</th>
          <th>Category</th>
          <th>Profile</th>
          <th>Tasks</th>
          <th>Success Rate</th>
          <th>Artifacts</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>
  </div>
</body>
</html>
"""

    def serve(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        """
        Start the dashboard HTTP server.

        Args:
            host: Interface to bind (default 127.0.0.1).
            port: TCP port for serving dashboard and report files.

        The server runs until interrupted (Ctrl+C), then closes gracefully.
        """
        webview = self

        class DashboardHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(webview.reports_dir), **kwargs)

            def do_GET(self):
                if self.path in ("/", "/index.html"):
                    html_content = webview._render_dashboard_html().encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(html_content)))
                    self.end_headers()
                    self.wfile.write(html_content)
                    return
                return super().do_GET()

        server = ThreadingHTTPServer((host, port), DashboardHandler)
        print(f"[*] Detective Joe Webview running at http://{host}:{port}")
        print("[*] Press Ctrl+C to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Webview stopped.")
        finally:
            server.server_close()
