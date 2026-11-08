"""Gamma Operations Suite: Automates generation, editing, exporting, and analytics."""

import urllib.request
import urllib.error
import json
import subprocess
import time
from pathlib import Path


def get_token():
    """Retrieve the active Gamma OAuth token from Keychain."""
    cmd = ['security', 'find-generic-password', '-s', 'Codex MCP Credentials', '-a', 'gamma|7921eb7bf9bf0a2e', '-w']
    raw = subprocess.check_output(cmd).decode().strip()
    data = json.loads(raw)
    return data['token_response']['access_token']


def call_mcp_tool(name: str, arguments: dict):
    """Call any tool on the official Gamma MCP endpoint."""
    token = get_token()
    req_body = {
        'jsonrpc': '2.0',
        'id': f'call-{name}-{int(time.time())}',
        'method': 'tools/call',
        'params': {
            'name': name,
            'arguments': arguments
        }
    }
    req = urllib.request.Request(
        'https://mcp.gamma.app/mcp',
        data=json.dumps(req_body).encode(),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        },
        method='POST'
    )
    resp_text = urllib.request.urlopen(req, timeout=60).read().decode()
    for line in resp_text.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])
    return {}


def wait_for_generation(gen_id: str, timeout_sec: int = 240):
    """Poll generation until completed."""
    print(f"[*] Polling generation {gen_id}...")
    start = time.time()
    while time.time() - start < timeout_sec:
        res = call_mcp_tool('get_generation_status', {'generationId': gen_id})
        content = res.get('result', {}).get('structuredContent', {})
        status = content.get('status')
        print(f"    - Status: {status}")
        if status == 'completed':
            return content
        elif status == 'failed':
            print(f"[-] Generation failed: {content.get('error')}")
            return content
        time.sleep(10)
    return {}


if __name__ == '__main__':
    print("[+] Gamma Operations Suite loaded.")
