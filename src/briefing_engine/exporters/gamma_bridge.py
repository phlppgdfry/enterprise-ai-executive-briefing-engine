"""Gamma Bridge: Dispatches generated presentation payloads to API, MCP, or local mock."""

import os
from typing import Dict, Any
from briefing_engine.models.presentation import PresentationDeck
from briefing_engine.integrations.gamma_client import GammaApiClient
from briefing_engine.integrations.gamma_mcp import GammaMcpClient
from briefing_engine.integrations.mock_gamma import MockGammaService


class GammaBridge:
    """Unified gateway for publishing decks to Gamma via preferred transport."""

    def __init__(self, provider: str = "mock", api_key: str = ""):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv("GAMMA_API_KEY", "")
        self.api_client = GammaApiClient(api_key=self.api_key)
        self.mcp_client = GammaMcpClient()
        self.mock_service = MockGammaService()

    def publish_deck(self, deck: PresentationDeck) -> Dict[str, Any]:
        """Deploy deck through the selected provider (mock, api, or mcp)."""
        payload = deck.to_gamma_payload()

        if self.provider == "api":
            if not self.api_key:
                return {
                    "error": True,
                    "message": "GAMMA_API_KEY environment variable is not set. Use provider='mock' for offline testing."
                }
            return self.api_client.create_generation(
                prompt_or_markdown=payload["markdown_content"],
                theme=deck.theme
            )

        elif self.provider == "mcp":
            return self.mcp_client.generate_presentation(
                title=deck.title,
                markdown_content=payload["markdown_content"],
                theme=deck.theme
            )

        else:
            # Default to mock
            result = self.mock_service.create_generation(
                prompt=payload["markdown_content"],
                theme=deck.theme
            )
            result["provider"] = "mock_simulator"
            result["note"] = "Generated via local deterministic simulator (0 credits consumed)."
            return result
