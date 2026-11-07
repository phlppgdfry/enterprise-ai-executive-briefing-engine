"""Unit tests for Strategy Consultant Agent."""

from briefing_engine.agents.business_analyst import BusinessAnalystAgent
from briefing_engine.agents.strategy_consultant import StrategyConsultantAgent


def test_strategy_consultant_pyramid_principle(sample_bundle):
    ba = BusinessAnalystAgent()
    analysis = ba.run(sample_bundle)

    strat_agent = StrategyConsultantAgent()
    strategy = strat_agent.run(analysis, sample_bundle)

    assert "2026-Q4" in strategy.situation
    assert len(strategy.strategic_pillars) == 3
    assert len(strategy.board_recommendations) >= 2
    assert len(strategy.required_decisions) >= 1
    assert "thesis" in strategy.executive_thesis.lower() or len(strategy.executive_thesis) > 20
