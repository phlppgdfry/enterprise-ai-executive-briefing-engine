"""Integration test for full end-to-end pipeline execution."""

from briefing_engine.orchestrator import BriefingOrchestrator


def test_full_pipeline_mock_execution(sample_bundle):
    orchestrator = BriefingOrchestrator(provider="mock")
    results = orchestrator.execute_pipeline(sample_bundle)

    assert results["status"] == "SUCCESS"
    assert results["period"] == "2026-Q4"

    # Verify audit gate passed
    audit = results["audit_report"]
    assert audit.passed_audit_gate is True

    # Verify deck generated
    deck = results["deck"]
    assert deck.total_cards() >= 7

    # Verify export outputs
    assert len(results["markdown"]) > 500
    assert "Executive Board Briefing" in results["markdown"]
    assert "<!DOCTYPE html>" in results["html"]
    assert "Gamma online" in results["publish_result"]["note"] or "mock_simulator" in results["publish_result"].get("provider", "")
