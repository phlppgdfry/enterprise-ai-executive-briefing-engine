"""Strategy Consultant Agent: Crafts executive narrative using the Pyramid Principle."""

from typing import List
from briefing_engine.agents.base import BaseAgent
from briefing_engine.models.analysis import (
    BusinessAnalysisOutput,
    StrategyConsultantOutput,
    StrategicPillar
)
from briefing_engine.models.raw_data import IngestionBundle


class StrategyConsultantAgent(BaseAgent):
    """Turns quantitative findings into a structured C-level executive briefing narrative."""

    def __init__(self):
        super().__init__(
            name="Executive Strategy Consultant Agent",
            role="Narrative Architecture, Pyramid Principle Structuring & Board Framing"
        )

    def run(self, analysis: BusinessAnalysisOutput, bundle: IngestionBundle) -> StrategyConsultantOutput:
        """Formulate executive thesis, strategic pillars, and governance action items."""

        # Situation
        situation = (
            f"During {analysis.period_label}, the organization demonstrated strong operational resilience, "
            f"achieving an overall operational health score of {analysis.operational_health_score}/100. "
            f"Core recurring revenue expanded with solid unit economics (LTV/CAC exceeding industry baselines)."
        )

        # Complication
        complications = []
        if analysis.growth_trends.get("revenue_qoq_pct"):
            complications.append(
                f"Sustaining {analysis.growth_trends['revenue_qoq_pct']}% QoQ growth requires scaling automated delivery "
                "to prevent operational bottlenecks and margin compression."
            )
        if bundle.project and bundle.project.overall_status in ("AMBER", "RED"):
            complications.append(
                f"Program execution for '{bundle.project.program_name}' is currently flagged as {bundle.project.overall_status}, "
                f"demanding targeted architectural intervention on critical dependency milestones."
            )
        if not complications:
            complications.append("Market competition requires accelerated digital core modernization and operational automation.")

        complication_text = " ".join(complications)

        # Resolution Strategy
        resolution = (
            "Execute a focused three-pillar roadmap: (1) Modernize core digital automation and integrations, "
            "(2) Optimize capital efficiency through batched architectural decoupling, and "
            "(3) Institute executive KPI governance with automated audit gates."
        )

        # Strategic Pillars
        pillars: List[StrategicPillar] = [
            StrategicPillar(
                title="Operational Excellence & Core Automation",
                rationale="Eliminate manual handoffs and legacy process friction to protect gross margins above 75%.",
                action_items=[
                    "Scale asynchronous event-driven integrations across operational endpoints.",
                    "Automate gate and dwell-time monitoring to sustain sub-20 minute turnaround times.",
                    "Embed continuous data quality validation rules before upstream ERP ingestion."
                ],
                impact_level="CRITICAL"
            ),
            StrategicPillar(
                title="Capital Efficiency & Margin Expansion",
                rationale="Leverage software-defined workflows and API orchestration to lower cost-to-serve.",
                action_items=[
                    "Maintain net burn below target thresholds while extending cash runway past 20 months.",
                    "Prioritize enterprise accounts with superior LTV/CAC ratios (>4.0x).",
                    "Consolidate vendor infrastructure dependencies into unified cloud microservices."
                ],
                impact_level="HIGH"
            ),
            StrategicPillar(
                title="Scalable Technology Governance",
                rationale="Ensure 99.9%+ platform availability with deterministic quality assurance and compliance.",
                action_items=[
                    "Enforce zero-unverified-claims policy across all management telemetry.",
                    "Complete final cutover of legacy interfaces with zero business disruption.",
                    "Deploy automated executive briefings via Gamma MCP for board-level transparency."
                ],
                impact_level="HIGH"
            )
        ]

        # Board recommendations & required decisions
        recommendations = [
            "Approve the Q1-Q2 2027 Technology Capital Allocation of €450k for final legacy decommissioning.",
            "Authorize the expansion of the enterprise automation footprint to secondary commercial terminals.",
            "Endorse the transition to real-time automated board reporting via Gamma MCP."
        ]

        decisions = [
            "Formal sign-off on Milestone M4/M5 dependency mitigation plan.",
            "Approval of updated risk mitigation budget for EDI parser batching."
        ]

        thesis = (
            f"The business is positioned for profitable, scalable expansion in {analysis.period_label}. "
            "Execution must prioritize automated infrastructure resilience and strict governance."
        )

        return StrategyConsultantOutput(
            executive_thesis=thesis,
            situation=situation,
            complication=complication_text,
            resolution_strategy=resolution,
            strategic_pillars=pillars,
            board_recommendations=recommendations,
            required_decisions=decisions
        )
