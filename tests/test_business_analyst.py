"""Unit tests for Business Analyst Agent."""

from briefing_engine.agents.business_analyst import BusinessAnalystAgent


def test_business_analyst_kpi_computation(sample_bundle):
    agent = BusinessAnalystAgent()
    analysis = agent.run(sample_bundle)

    assert analysis.period_label == "2026-Q4"
    assert analysis.operational_health_score >= 80.0
    assert len(analysis.kpis) >= 5

    # Check revenue KPI
    rev_kpi = next((k for k in analysis.kpis if k.key == "revenue"), None)
    assert rev_kpi is not None
    assert rev_kpi.numeric_value == 1950000.0
    assert rev_kpi.target_value == 1800000.0
    assert rev_kpi.variance_pct > 0
    assert rev_kpi.status == "EXCEEDED"

    # Check gross margin KPI
    margin_kpi = next((k for k in analysis.kpis if k.key == "gross_margin"), None)
    assert margin_kpi is not None
    assert margin_kpi.numeric_value == 78.5

    # Check growth trends
    assert "revenue_qoq_pct" in analysis.growth_trends
    assert analysis.growth_trends["revenue_qoq_pct"] > 0
