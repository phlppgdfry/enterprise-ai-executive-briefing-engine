"""Unit tests for Presentation Planner Agent."""

from briefing_engine.agents.business_analyst import BusinessAnalystAgent
from briefing_engine.agents.strategy_consultant import StrategyConsultantAgent
from briefing_engine.agents.presentation_planner import PresentationPlannerAgent
from briefing_engine.models.presentation import CardLayout


def test_presentation_planner_card_generation(sample_bundle):
    ba = BusinessAnalystAgent()
    analysis = ba.run(sample_bundle)

    strat = StrategyConsultantAgent()
    strategy = strat.run(analysis, sample_bundle)

    planner = PresentationPlannerAgent()
    deck = planner.run(analysis, strategy, sample_bundle)

    assert deck.total_cards() >= 7
    assert deck.theme == "enterprise_dark"

    # Verify layouts
    layouts = [c.layout for c in deck.cards]
    assert CardLayout.TITLE_HERO in layouts
    assert CardLayout.EXECUTIVE_SUMMARY in layouts
    assert CardLayout.METRIC_GRID in layouts
    assert CardLayout.TIMELINE_ROADMAP in layouts

    # Verify Markdown export
    first_card_md = deck.cards[0].to_gamma_markdown()
    assert "## " in first_card_md
    assert "notes:" in first_card_md
