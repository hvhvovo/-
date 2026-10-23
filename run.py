import argparse
import json
import datetime
from html import escape
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('mode', nargs='?', choices=['offline', 'read', 'full'], default='offline')
mode = parser.parse_args().mode
os.chdir(root)
reports = root / 'reports'; reports.mkdir(exist_ok=True)
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
xml = reports / f'{mode}-{stamp}.xml'
cmd = [sys.executable, '-m', 'pytest', '-v', '--tb=short', f'--junitxml={xml}']
if mode != 'offline': cmd.append('--live')
if mode == 'full': cmd.append('--allow-write')
case_path = reports / f'{mode}-{stamp}-cases.json'
env = dict(os.environ, BOOKING_CASE_RESULTS=str(case_path))
result = subprocess.run(cmd, env=env)
if xml.exists():
    rows = []; counts = dict(passed=0, failed=0, error=0, skipped=0)
    for case in ET.parse(xml).iter('testcase'):
        status, detail = 'passed', ''
        for tag, state in [('failure', 'failed'), ('error', 'error'), ('skipped', 'skipped')]:
            node = case.find(tag)
            if node is not None:
                status, detail = state, node.get('message', '') + '\n' + (node.text or '')
                break
        counts[status] += 1
        rows.append('<tr><td>' + escape(case.get('classname', '') + '::' + case.get('name', ''))
            + '</td><td>' + status + '</td><td><pre>' + escape(detail) + '</pre></td></tr>')
    html = '<!doctype html><meta charset="utf-8"><title>Booking API report</title>'
    html += '<style>body{font:15px sans-serif;margin:30px}td,th{padding:10px;border:1px solid #ccc}table{border-collapse:collapse}pre{white-space:pre-wrap;max-width:700px}</style>'
    html += '<h1>Booking API test report</h1><p>Mode: ' + mode + '</p><p>' + escape(str(counts)) + '</p>'
    if case_path.exists():
        case_data = json.loads(case_path.read_text(encoding='utf-8'))
        groups = {}
        for case in case_data['cases']:
            states = case['phases'].values()
            state = 'failed' if 'failed' in states else ('skipped' if 'skipped' in states else 'passed')
            group = groups.setdefault(case['kind'], {'passed': 0, 'failed': 0, 'skipped': 0})
            group[state] += 1
        html += '<h2>Offline / live</h2><pre>' + escape(json.dumps(groups, indent=2)) + '</pre>'
        print('Results by group:', groups)
    html += '<p>Offline tests validate helpers only. Skipped is not passed. Shared API tests do not establish production correctness or capacity.</p>'
    html += '<table><tr><th>Test</th><th>Status</th><th>Details</th></tr>' + ''.join(rows) + '</table>'
    output = reports / f'{mode}-{stamp}.html'; output.write_text(html, encoding='utf-8')
    print('HTML report:', output)
    print('Request metadata:', case_path)
sys.exit(result.returncode)
