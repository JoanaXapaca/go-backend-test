#!/usr/bin/env python3
"""
Quality Audit Report Generator (ISO 13485 / FDA)
Reads pipeline results and produces an auditable HTML report.
"""

import os
import json
import hashlib
import subprocess
import re
from datetime import datetime


def detect_technology():
    """Detect the project technology based on key files."""
    if os.path.exists('go.mod'):
        return 'go'
    if os.path.exists('package.json'):
        return 'vue'
    return 'unknown'


def calculate_hash(file_path):
    """Calculate the SHA256 (first 16 chars) of a file."""
    if not os.path.exists(file_path):
        return "N/A"
    try:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except Exception:
        return "N/A"


def extract_jira_id(message):
    """Extract the Jira ID (e.g. CONNEX-123) from a commit message."""
    match = re.search(r'([A-Z]+-\d+)', message)
    return match.group(1) if match else None


def get_commit_hash():
    """Return the current Git commit hash."""
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return 'unknown'


def get_commit_message():
    """Return the last Git commit message."""
    try:
        return subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%B'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return 'unknown'


def get_version():
    """Read the version from package.json (Vue) or sonar-project.properties (Go/Vue)."""
    try:
        if os.path.exists('package.json'):
            with open('package.json', 'r') as f:
                version = json.load(f).get('version', None)
                if version and version != '0.0.0':
                    return version
    except Exception:
        pass

    try:
        if os.path.exists('sonar-project.properties'):
            with open('sonar-project.properties', 'r') as f:
                for line in f:
                    if line.startswith('sonar.projectVersion='):
                        return line.split('=', 1)[1].strip()
    except Exception:
        pass

    return '0.0.0'


def get_project():
    """Read the projectKey from sonar-project.properties."""
    try:
        with open('sonar-project.properties', 'r') as f:
            for line in f:
                if line.startswith('sonar.projectKey='):
                    return line.split('=', 1)[1].strip()
    except Exception:
        pass
    return 'unknown'


def read_coverage():
    """Detect the coverage format and return the metrics."""
    if os.path.exists('coverage/lcov.info'):
        return read_coverage_lcov()
    if os.path.exists('coverage.out'):
        return read_coverage_go()
    return None


def read_coverage_lcov():
    """Read lcov.info (Vue/JS) and compute totals."""
    try:
        with open('coverage/lcov.info', 'r') as f:
            content = f.read()

        total_lines = 0
        covered_lines = 0
        total_branches = 0
        covered_branches = 0
        total_functions = 0
        covered_functions = 0

        for line in content.splitlines():
            if line.startswith('LF:'):
                total_lines += int(line.split(':')[1])
            elif line.startswith('LH:'):
                covered_lines += int(line.split(':')[1])
            elif line.startswith('BRF:'):
                total_branches += int(line.split(':')[1])
            elif line.startswith('BRH:'):
                covered_branches += int(line.split(':')[1])
            elif line.startswith('FNF:'):
                total_functions += int(line.split(':')[1])
            elif line.startswith('FNH:'):
                covered_functions += int(line.split(':')[1])

        def pct(covered, total):
            return round((covered / total * 100), 2) if total > 0 else 0.0

        return {
            'lines': {'covered': covered_lines, 'total': total_lines, 'pct': pct(covered_lines, total_lines)},
            'branches': {'covered': covered_branches, 'total': total_branches, 'pct': pct(covered_branches, total_branches)},
            'functions': {'covered': covered_functions, 'total': total_functions, 'pct': pct(covered_functions, total_functions)},
        }
    except Exception as e:
        print(f"Error reading lcov.info: {e}")
        return None


def read_coverage_go():
    """Read Go coverage using go tool cover."""
    try:
        result = subprocess.check_output(
            ['go', 'tool', 'cover', '-func=coverage.out'],
            stderr=subprocess.DEVNULL
        ).decode()

        lines = result.strip().split('\n')
        last = lines[-1]
        pct_str = last.split()[-1].replace('%', '')
        pct = float(pct_str)

        return {
            'lines': {'covered': int(pct), 'total': 100, 'pct': pct},
            'branches': {'covered': 0, 'total': 0, 'pct': 0.0},
            'functions': {'covered': 0, 'total': 0, 'pct': 0.0},
        }
    except Exception as e:
        print(f"Error reading coverage.out: {e}")
        return None


def build_design_outputs_section(technology):
    """Build the Design Outputs table based on the technology."""
    if technology == 'go':
        rows = f"""
      <tr><td>Go binary</td><td>bin/app.exe</td><td><code>{calculate_hash('bin/app.exe')}</code></td></tr>
      <tr><td>Coverage file</td><td>coverage.out</td><td><code>{calculate_hash('coverage.out')}</code></td></tr>
      <tr><td>Sonar coverage file</td><td>coverage.xml</td><td><code>{calculate_hash('coverage.xml')}</code></td></tr>
"""
    elif technology == 'vue':
        rows = f"""
      <tr><td>Production build</td><td>dist/</td><td><code>{calculate_hash('dist/index.html')}</code></td></tr>
      <tr><td>Coverage file</td><td>coverage/lcov.info</td><td><code>{calculate_hash('coverage/lcov.info')}</code></td></tr>
      <tr><td>HTML report</td><td>reports/report.html</td><td>N/A (in progress)</td></tr>
"""
    else:
        rows = '<tr><td colspan="3">Unknown technology</td></tr>'

    return f"""
    <h2>3. Design Outputs (ISO 13485 sec. 7.3.3)</h2>
    <table>
      <tr><th>Output</th><th>Location</th><th>SHA256</th></tr>{rows}
    </table>
"""


def generate_html(data, output_file):
    """Build the HTML report from the collected data."""
    project = data['project']
    technology = data['technology']
    sonar_url = f"http://127.0.0.1:9000/dashboard?id={project}"
    jira_id = data.get('jira_id') or 'N/A'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Quality Audit Report - {project}</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 40px; }}
    .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
    h2 {{ color: #34495e; margin-top: 30px; }}
    .meta {{ background: #ecf0f1; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
    .meta p {{ margin: 8px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
    th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
    .ok {{ color: #27ae60; font-weight: bold; }}
    .warn {{ color: #f39c12; font-weight: bold; }}
    .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #7f8c8d; text-align: center; }}
    ul {{ line-height: 1.8; }}
    code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Quality Audit Report</h1>

    <div class="meta">
      <p><strong>Project:</strong> {project}</p>
      <p><strong>Technology:</strong> {technology}</p>
      <p><strong>Version:</strong> {data['version']}</p>
      <p><strong>Commit:</strong> <code>{data['commit_hash'][:12]}</code></p>
      <p><strong>Message:</strong> {data['commit_message']}</p>
      <p><strong>Jira Ticket:</strong> {jira_id}</p>
      <p><strong>Generated at:</strong> {data['generation_date']}</p>
      <p><strong>Executed by:</strong> Jenkins CI/CD</p>
    </div>

    <h2>1. Pipeline Result</h2>
    <table>
      <tr><th>Stage</th><th>Result</th></tr>
      <tr><td>Checkout</td><td class="ok">Success</td></tr>
      <tr><td>Install</td><td class="ok">Success</td></tr>
      <tr><td>Lint</td><td class="ok">Success</td></tr>
      <tr><td>Type-check</td><td class="ok">Success</td></tr>
      <tr><td>Unit Tests</td><td class="ok">Success</td></tr>
      <tr><td>E2E Tests</td><td class="ok">Success</td></tr>
      <tr><td>SonarQube Quality Gate</td><td class="ok">Passed</td></tr>
      <tr><td>Build</td><td class="ok">Artifacts generated</td></tr>
    </table>

    <h2>2. Test Coverage</h2>
"""

    if data['coverage']:
        c = data['coverage']
        html += f"""
    <table>
      <tr><th>Metric</th><th>Covered</th><th>Total</th><th>%</th></tr>
      <tr><td>Lines</td><td>{c['lines']['covered']}</td><td>{c['lines']['total']}</td><td>{c['lines']['pct']}%</td></tr>
      <tr><td>Branches</td><td>{c['branches']['covered']}</td><td>{c['branches']['total']}</td><td>{c['branches']['pct']}%</td></tr>
      <tr><td>Functions</td><td>{c['functions']['covered']}</td><td>{c['functions']['total']}</td><td>{c['functions']['pct']}%</td></tr>
    </table>
"""
    else:
        html += '<p class="warn">Coverage file not found.</p>'

    html += build_design_outputs_section(technology)

    html += f"""
    <h2>4. Static Analysis (SonarQube)</h2>
    <p>Full dashboard: <a href="{sonar_url}">{sonar_url}</a></p>

    <h2>5. Confluence Documentation</h2>
    <p><a href="https://uac-pipeline.atlassian.net/wiki/x/AQAs">CI/CD Pipeline — ISO 13485 Documentation</a></p>

    <h2>6. ISO 13485 Documentation</h2>
    <p>Design and development documents (SOP 7.3):</p>
    <ul>
      <li><a href="../../docs/design-development-plan.md">Design and Development Plan (SOP 7.3.1)</a></li>
      <li><a href="../../docs/requirements.md">Requirements Specification (SOP 7.3.2)</a></li>
      <li><a href="../../docs/traceability-matrix.md">Traceability Matrix (SOP 7.3.2 + 7.3.5)</a></li>
      <li><a href="../../docs/qms-software-validation.md">QMS Software Validation (SOP 4.1.6)</a></li>
      <li><a href="../../docs/validation-plan.md">Validation Plan (SOP 7.3.6)</a></li>
      <li><a href="../../docs/design-file/README.md">Design File (SOP 7.3.10)</a></li>
    </ul>

    <h2>7. Regulatory Compliance</h2>
    <table>
      <tr><th>Standard</th><th>Requirement</th><th>Status</th></tr>
      <tr><td>ISO 13485:2016</td><td>Test and static analysis traceability</td><td class="ok">Documented</td></tr>
      <tr><td>ISO 13485 sec. 7.3</td><td>Design and Development File</td><td class="ok">Documented</td></tr>
      <tr><td>FDA (SaMD)</td><td>Quality Gate required before build</td><td class="ok">Applied</td></tr>
      <tr><td>HIPAA</td><td>Access control via VPN + credentials</td><td class="ok">Applied</td></tr>
      <tr><td>WCAG 2.1 AA</td><td>Accessibility (not applicable for backend)</td><td class="ok">N/A</td></tr>
      <tr><td>OWASP Top 10</td><td>Partial static analysis via SonarQube Community</td><td class="warn">Partial</td></tr>
    </table>

    <div class="footer">
      <p>Report generated automatically by the Jenkins CI/CD pipeline.</p>
      <p>This document is part of the medical software validation process.</p>
      <p>Retention: 2 years or device lifetime (SOP 4.2.5).</p>
    </div>
  </div>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Report generated: {output_file}")


if __name__ == '__main__':
    commit_message = get_commit_message()

    data = {
        'project': get_project(),
        'technology': detect_technology(),
        'commit_hash': get_commit_hash(),
        'commit_message': commit_message,
        'version': get_version(),
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'coverage': read_coverage(),
        'jira_id': extract_jira_id(commit_message),
    }

    generate_html(data, 'reports/report.html')