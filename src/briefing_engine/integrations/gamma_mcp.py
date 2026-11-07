"""Official Gamma MCP Server Client: Connects to https://mcp.gamma.app/mcp"""

import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional


class GammaMcpClient:
    """Client for orchestrating presentations via Gamma's official MCP endpoint."""

    ENDPOINT = "https://mcp.gamma.app/mcp"

    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or self.ENDPOINT

    def list_tools(self) -> Dict[str, Any]:
        """Request available MCP tools from the Gamma MCP server."""
        payload = {
            "jsonrpc": "2.0",
            "id": "list-tools-req",
            "method": "tools/list",
            "params": {}
        }
        return self._send_rpc(payload)

    def generate_presentation(self, title: str, markdown_content: str, theme: str = "enterprise_dark") -> Dict[str, Any]:
        """Invoke the Gamma MCP tool `generate_presentation`."""
        payload = {
            "jsonrpc": "2.0",
            "id": f"gen-{int(__import__('time').time())}",
            "method": "tools/call",
            "params": {
                "name": "generate_presentation",
                "arguments": {
                    "title": title,
                    "content": markdown_content,
                    "theme": theme,
                    "format": "presentation"
                }
            }
        }
        return self._send_rpc(payload)

    def export_presentation(self, presentation_id: str, format_type: str = "pdf") -> Dict[str, Any]:
        """Invoke the Gamma MCP tool `export_presentation`."""
        payload = {
            "jsonrpc": "2.0",
            "id": f"exp-{int(__import__('time').time())}",
            "method": "tools/call",
            "params": {
                "name": "export_presentation",
                "arguments": {
                    "presentation_id": presentation_id,
                    "format": format_type
                }
            }
        }
        return self._send_rpc(payload)

    def _send_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # Handle OAuth 401 requirement gracefully
            return {
                "error": True,
                "status_code": e.code,
                "requires_auth": e.code == 401,
                "message": f"MCP endpoint returned HTTP {e.code}: {e.reason}. OAuth authorization required in MCP client."
            }
        except Exception as ex:
            return {
                "error": True,
                "message": f"Failed to connect to Gamma MCP: {str(ex)}"
            }
