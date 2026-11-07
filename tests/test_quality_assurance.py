"""Unit tests for Quality Assurance Agent."""

from briefing_engine.agents.business_analyst import BusinessAnalystAgent
from briefing_engine.agents.strategy_consultant import StrategyConsultantAgent
from briefing_engine.agents.presentation_planner import PresentationPlannerAgent
from briefing_engine.agents.quality_assurance import QualityAssuranceAgent


def test_quality_assurance_audit_gate(sample_bundle):
    ba = BusinessAnalystAgent()
    analysis = ba.run(sample_bundle)

    strat = StrategyConsultantAgent()
    strategy = strat.run(analysis, sample_bundle)

    planner = PresentationPlannerAgent()
    deck = planner.run(analysis, strategy, sample_bundle)

    qa = QualityAssuranceAgent()
    report = qa.run(deck, analysis, sample_bundle)

    assert report.total_claims_audited > 0
    assert report.verified_claims_count > 0
    assert report.audit_score_pct >= 85.0
    assert report.passed_audit_gate is True
    assert "PASSED" in report.summary_status()
