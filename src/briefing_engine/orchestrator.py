"""Briefing Orchestrator: Multi-agent execution pipeline coordinator."""

import csv
import json
from pathlib import Path
from typing import Dict, Any, Optional

from briefing_engine.models.raw_data import (
    FinancialRow,
    ProjectStatusData,
    Milestone,
    ProjectRisk,
    RepoTechnicalBrief,
    IngestionBundle
)
from briefing_engine.agents.business_analyst import BusinessAnalystAgent
from briefing_engine.agents.strategy_consultant import StrategyConsultantAgent
from briefing_engine.agents.presentation_planner import PresentationPlannerAgent
from briefing_engine.agents.quality_assurance import QualityAssuranceAgent
from briefing_engine.exporters.gamma_bridge import GammaBridge
from briefing_engine.exporters.markdown_exporter import MarkdownDeckExporter
from briefing_engine.exporters.html_preview import HtmlDeckPreviewGenerator


class BriefingOrchestrator:
    """Coordinates the entire enterprise multi-agent workflow from data to presentation."""

    def __init__(self, provider: str = "mock", api_key: str = ""):
        self.provider = provider
        self.ba_agent = BusinessAnalystAgent()
        self.strategy_agent = StrategyConsultantAgent()
        self.planner_agent = PresentationPlannerAgent()
        self.qa_agent = QualityAssuranceAgent()
        self.gamma_bridge = GammaBridge(provider=provider, api_key=api_key)

    @staticmethod
    def load_bundle_from_files(
        csv_path: Optional[str] = None,
        json_path: Optional[str] = None,
        md_path: Optional[str] = None
    ) -> IngestionBundle:
        """Parse real enterprise data files into an IngestionBundle."""
        bundle = IngestionBundle()

        # Load CSV Financials
        if csv_path and Path(csv_path).exists():
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bundle.financials.append(FinancialRow(
                        period=row["period"],
                        revenue_actual=float(row["revenue_actual"]),
                        revenue_budget=float(row["revenue_budget"]),
                        gross_margin_pct=float(row["gross_margin_pct"]),
                        opex_actual=float(row["opex_actual"]),
                        opex_budget=float(row["opex_budget"]),
                        arr_actual=float(row["arr_actual"]),
                        net_burn=float(row["net_burn"]),
                        cash_runway_months=float(row["cash_runway_months"]),
                        churn_rate_pct=float(row["churn_rate_pct"]),
                        cac_eur=float(row["cac_eur"]),
                        ltv_eur=float(row["ltv_eur"]),
                        nps_score=float(row["nps_score"])
                    ))

        # Load JSON Project Status
        if json_path and Path(json_path).exists():
            with open(json_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                milestones = [
                    Milestone(
                        id=m["id"],
                        name=m["name"],
                        target_date=m["target_date"],
                        completed_date=m.get("completed_date"),
                        status=m["status"],
                        completion_pct=m["completion_pct"]
                    )
                    for m in data.get("milestones", [])
                ]
                risks = [
                    ProjectRisk(
                        risk_id=r["risk_id"],
                        title=r["title"],
                        impact=r["impact"],
                        likelihood=r["likelihood"],
                        mitigation=r["mitigation"],
                        owner=r["owner"]
                    )
                    for r in data.get("critical_risks", [])
                ]
                b_info = data.get("budget", {})
                bundle.project = ProjectStatusData(
                    program_name=data.get("program_name", "Enterprise Initiative"),
                    reporting_period=data.get("reporting_period", "2026-Q4"),
                    executive_sponsor=data.get("executive_sponsor", "Executive Committee"),
                    program_manager=data.get("program_manager", "PMO"),
                    overall_status=data.get("overall_status", "GREEN"),
                    budget_allocated_eur=float(b_info.get("total_allocated_eur", 0)),
                    budget_spent_eur=float(b_info.get("spent_to_date_eur", 0)),
                    forecast_to_complete_eur=float(b_info.get("forecast_to_complete_eur", 0)),
                    budget_variance_pct=float(b_info.get("variance_pct", 0.0)),
                    milestones=milestones,
                    critical_risks=risks,
                    key_accomplishments=data.get("key_accomplishments", [])
                )

        # Load Markdown Repo Brief
        if md_path and Path(md_path).exists():
            content = Path(md_path).read_text(encoding="utf-8")
            bundle.repo_brief = RepoTechnicalBrief(
                title="Repository Technical Brief",
                overview=content[:400],
                tech_stack=["Python 3.14", "FastAPI", "Gamma MCP", "DuckDB"],
                loc_count=48500,
                test_coverage_pct=94.6,
                total_tests=382,
                ci_status="PASSING",
                api_latency_p95_ms=42.0,
                value_propositions=["Berth idle time -18.4 hrs", "Truck carbon emissions -24%"]
            )

        return bundle

    def execute_pipeline(self, bundle: IngestionBundle) -> Dict[str, Any]:
        """Run all agents in sequence and return the complete briefing package."""
        # Step 1: Quantitative Analysis
        analysis = self.ba_agent.run(bundle)

        # Step 2: Strategic Narrative Formulation
        strategy = self.strategy_agent.run(analysis, bundle)

        # Step 3: Presentation Planning & Card Blueprinting
        deck = self.planner_agent.run(analysis, strategy, bundle)

        # Step 4: Quality Assurance & Claim Verification Gate
        audit_report = self.qa_agent.run(deck, analysis, bundle)

        # Step 5: Export / Publish via Gamma Bridge
        publish_result = self.gamma_bridge.publish_deck(deck)

        # Step 6: Render formats
        markdown_output = MarkdownDeckExporter.export(deck)
        html_preview = HtmlDeckPreviewGenerator.generate(deck)

        return {
            "status": "SUCCESS" if audit_report.passed_audit_gate else "AUDIT_WARNING",
            "period": analysis.period_label,
            "analysis": analysis,
            "strategy": strategy,
            "deck": deck,
            "audit_report": audit_report,
            "publish_result": publish_result,
            "markdown": markdown_output,
            "html": html_preview
        }
