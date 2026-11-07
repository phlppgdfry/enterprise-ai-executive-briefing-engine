"""Unit tests for Gamma MCP Client."""

from unittest.mock import patch, MagicMock
from briefing_engine.integrations.gamma_mcp import GammaMcpClient


def test_gamma_mcp_client_rpc_formatting():
    client = GammaMcpClient()

    # Mock urllib response for deterministic fast testing
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"jsonrpc": "2.0", "result": {"tools": [{"name": "generate_presentation"}]}}'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        res = client.list_tools()
        assert isinstance(res, dict)
        assert "result" in res
        assert res["result"]["tools"][0]["name"] == "generate_presentation"

    # Test error / auth handling when 401 is returned
    with patch("urllib.request.urlopen", side_effect=__import__("urllib.error").error.HTTPError("url", 401, "Unauthorized", {}, None)):
        err_res = client.list_tools()
        assert err_res.get("requires_auth") is True
        assert err_res.get("status_code") == 401
