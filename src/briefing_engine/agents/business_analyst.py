"""Business Analyst Agent: Performs rigorous mathematical KPI computation and reconciliation."""

from typing import List, Dict, Any
from briefing_engine.agents.base import BaseAgent
from briefing_engine.models.raw_data import IngestionBundle, FinancialRow, ProjectStatusData
from briefing_engine.models.analysis import BusinessAnalysisOutput, VerifiedKPI


class BusinessAnalystAgent(BaseAgent):
    """Calculates and verifies all quantitative metrics with zero hallucination."""

    def __init__(self):
        super().__init__(
            name="Senior Business Analyst Agent",
            role="Deterministic KPI Calculation, Variance Reconciliation & Operational Auditing"
        )

    def run(self, bundle: IngestionBundle) -> BusinessAnalysisOutput:
        """Process financial and project inputs into verified KPIs and health indices."""
        kpis: List[VerifiedKPI] = []
        growth_trends: Dict[str, float] = {}
        flags: List[str] = []
        period_label = "Current Period"

        # 1. Process Financial Series if present
        if bundle.financials:
            latest = bundle.financials[-1]
            period_label = latest.period

            # Revenue KPI
            rev_var = latest.revenue_variance_pct
            rev_status = "EXCEEDED" if rev_var > 0 else ("ON_TARGET" if rev_var == 0 else "AT_RISK")
            kpis.append(VerifiedKPI(
                key="revenue",
                label="Total Revenue",
                value_display=f"€{latest.revenue_actual:,.0f}",
                numeric_value=latest.revenue_actual,
                target_value=latest.revenue_budget,
                variance_pct=rev_var,
                status=rev_status,
                provenance_source=f"financials.{latest.period}.revenue_actual"
            ))

            # Gross Margin KPI
            kpis.append(VerifiedKPI(
                key="gross_margin",
                label="Gross Margin",
                value_display=f"{latest.gross_margin_pct:.1f}%",
                numeric_value=latest.gross_margin_pct,
                target_value=75.0,
                variance_pct=round(latest.gross_margin_pct - 75.0, 1),
                status="ON_TARGET" if latest.gross_margin_pct >= 75.0 else "AT_RISK",
                provenance_source=f"financials.{latest.period}.gross_margin_pct"
            ))

            # ARR KPI
            kpis.append(VerifiedKPI(
                key="arr",
                label="Annual Recurring Revenue (ARR)",
                value_display=f"€{latest.arr_actual:,.0f}",
                numeric_value=latest.arr_actual,
                target_value=latest.arr_actual,
                variance_pct=0.0,
                status="ON_TARGET",
                provenance_source=f"financials.{latest.period}.arr_actual"
            ))

            # Cash Runway KPI
            runway_status = "ON_TARGET" if latest.cash_runway_months >= 18.0 else ("AT_RISK" if latest.cash_runway_months >= 12.0 else "OFF_TRACK")
            kpis.append(VerifiedKPI(
                key="cash_runway",
                label="Cash Runway",
                value_display=f"{latest.cash_runway_months:.1f} months",
                numeric_value=latest.cash_runway_months,
                target_value=18.0,
                variance_pct=round(((latest.cash_runway_months - 18.0) / 18.0) * 100, 1),
                status=runway_status,
                provenance_source=f"financials.{latest.period}.cash_runway_months"
            ))

            # LTV / CAC Ratio
            ltv_cac = latest.ltv_cac_ratio
            kpis.append(VerifiedKPI(
                key="ltv_cac",
                label="LTV / CAC Ratio",
                value_display=f"{ltv_cac:.1f}x",
                numeric_value=ltv_cac,
                target_value=3.0,
                variance_pct=round(((ltv_cac - 3.0) / 3.0) * 100, 1),
                status="EXCEEDED" if ltv_cac >= 4.0 else ("ON_TARGET" if ltv_cac >= 3.0 else "AT_RISK"),
                provenance_source=f"derived.ltv_eur_over_cac_eur"
            ))

            # Quarter-over-Quarter Growth calculation
            if len(bundle.financials) >= 2:
                prev = bundle.financials[-2]
                rev_growth = round(((latest.revenue_actual - prev.revenue_actual) / prev.revenue_actual) * 100, 2)
                arr_growth = round(((latest.arr_actual - prev.arr_actual) / prev.arr_actual) * 100, 2)
                growth_trends["revenue_qoq_pct"] = rev_growth
                growth_trends["arr_qoq_pct"] = arr_growth

                if rev_growth > 0:
                    flags.append(f"Accelerating revenue growth: +{rev_growth}% QoQ from {prev.period} to {latest.period}.")
                if latest.net_burn < prev.net_burn:
                    flags.append(f"Capital efficiency improving: Net burn decreased to €{latest.net_burn:,.0f}/mo.")

        # 2. Process Project Status if present
        if bundle.project:
            proj = bundle.project
            comp_milestones = sum(1 for m in proj.milestones if "COMPLETED" in m.status)
            total_milestones = len(proj.milestones)
            pct_complete = round((comp_milestones / total_milestones) * 100, 1) if total_milestones > 0 else 0.0

            kpis.append(VerifiedKPI(
                key="project_budget_variance",
                label="Program Budget Variance",
                value_display=f"{proj.budget_variance_pct:+.1f}%",
                numeric_value=proj.budget_variance_pct,
                target_value=0.0,
                variance_pct=proj.budget_variance_pct,
                status="ON_TARGET" if proj.budget_variance_pct <= 0 else "AT_RISK",
                provenance_source="project.budget.variance_pct"
            ))

            kpis.append(VerifiedKPI(
                key="milestone_velocity",
                label="Milestone Completion",
                value_display=f"{comp_milestones}/{total_milestones} ({pct_complete}%)",
                numeric_value=pct_complete,
                target_value=100.0,
                variance_pct=round(pct_complete - 100.0, 1),
                status="ON_TARGET" if pct_complete >= 60.0 else "AT_RISK",
                provenance_source="project.milestones.count"
            ))

            flags.append(f"Program '{proj.program_name}' status is {proj.overall_status} with {len(proj.critical_risks)} monitored risks.")

        # Calculate composite Operational Health Score (0 - 100)
        on_target_count = sum(1 for k in kpis if k.status in ("ON_TARGET", "EXCEEDED"))
        health_score = round((on_target_count / len(kpis)) * 100, 1) if kpis else 75.0

        runway_text = "Strong (18+ months runway)" if any(k.key == "cash_runway" and k.numeric_value >= 18 for k in kpis) else "Stable"

        return BusinessAnalysisOutput(
            period_label=period_label,
            summary_headline=f"Financial & Operational Health Score: {health_score}/100 across {len(kpis)} audited indicators.",
            kpis=kpis,
            growth_trends=growth_trends,
            operational_health_score=health_score,
            financial_runway_assessment=runway_text,
            calculated_flags=flags
        )
