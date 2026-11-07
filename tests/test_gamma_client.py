"""Unit tests for Gamma API Client and Mock Service."""

from briefing_engine.integrations.gamma_client import GammaApiClient
from briefing_engine.integrations.mock_gamma import MockGammaService


def test_mock_gamma_service_lifecycle():
    service = MockGammaService()

    # Create generation
    gen = service.create_generation(prompt="Executive Briefing", theme="enterprise_dark")
    assert gen["status"] == "COMPLETED"
    assert "mock-gamma-" in gen["id"]
    assert "https://gamma.app/docs/" in gen["url"]

    # Status check
    status = service.get_generation_status(gen["id"])
    assert status["id"] == gen["id"]

    # Export check
    exp = service.export_deck(gen["id"], export_format="pdf")
    assert exp["status"] == "READY"
    assert exp["format"] == "pdf"


def test_gamma_api_client_error_handling_without_key():
    from unittest.mock import patch
    import urllib.error
    client = GammaApiClient(api_key="invalid-test-key")
    with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 401, "Unauthorized", {}, None)):
        res = client.create_generation("Sample prompt")
        assert res.get("error") is True
        assert res.get("status_code") == 401
