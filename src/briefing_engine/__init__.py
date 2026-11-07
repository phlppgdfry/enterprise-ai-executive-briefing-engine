"""Enterprise AI Executive Briefing Engine.

Automated multi-agent presentation generation with mathematical KPI validation,
audit-grade verification, and Gamma MCP & API integration.
"""

__version__ = "1.0.0"
__author__ = "Philippe Godfroy"

from briefing_engine.orchestrator import BriefingOrchestrator
from briefing_engine.models.presentation import PresentationDeck, GammaCard, CardLayout

__all__ = [
    "BriefingOrchestrator",
    "PresentationDeck",
    "GammaCard",
    "CardLayout",
]
