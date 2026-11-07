"""Data models for raw input ingestion (financials, projects, repositories)."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class FinancialRow:
    """A single quarter/period of enterprise financial performance."""
    period: str
    revenue_actual: float
    revenue_budget: float
    gross_margin_pct: float
    opex_actual: float
    opex_budget: float
    arr_actual: float
    net_burn: float
    cash_runway_months: float
    churn_rate_pct: float
    cac_eur: float
    ltv_eur: float
    nps_score: float

    @property
    def revenue_variance_pct(self) -> float:
        """Percentage variance between actual and budgeted revenue."""
        if self.revenue_budget == 0:
            return 0.0
        return round(((self.revenue_actual - self.revenue_budget) / self.revenue_budget) * 100, 2)

    @property
    def opex_variance_pct(self) -> float:
        """Percentage variance between actual and budgeted opex."""
        if self.opex_budget == 0:
            return 0.0
        return round(((self.opex_actual - self.opex_budget) / self.opex_budget) * 100, 2)

    @property
    def ltv_cac_ratio(self) -> float:
        """LTV to CAC efficiency ratio."""
        if self.cac_eur == 0:
            return 0.0
        return round(self.ltv_eur / self.cac_eur, 2)


@dataclass
class Milestone:
    """Project milestone tracking status."""
    id: str
    name: str
    target_date: str
    completed_date: Optional[str]
    status: str
    completion_pct: int


@dataclass
class ProjectRisk:
    """Identified project risk with mitigation strategy."""
    risk_id: str
    title: str
    impact: str
    likelihood: str
    mitigation: str
    owner: str


@dataclass
class ProjectStatusData:
    """Enterprise transformation project status report."""
    program_name: str
    reporting_period: str
    executive_sponsor: str
    program_manager: str
    overall_status: str
    budget_allocated_eur: float
    budget_spent_eur: float
    forecast_to_complete_eur: float
    budget_variance_pct: float
    milestones: List[Milestone] = field(default_factory=list)
    critical_risks: List[ProjectRisk] = field(default_factory=list)
    key_accomplishments: List[str] = field(default_factory=list)


@dataclass
class RepoTechnicalBrief:
    """Source code repository metrics and architecture analysis."""
    title: str
    overview: str
    tech_stack: List[str] = field(default_factory=list)
    loc_count: int = 0
    test_coverage_pct: float = 0.0
    total_tests: int = 0
    ci_status: str = "UNKNOWN"
    api_latency_p95_ms: float = 0.0
    value_propositions: List[str] = field(default_factory=list)


@dataclass
class IngestionBundle:
    """Unified container for all enterprise data feeds provided to the engine."""
    financials: List[FinancialRow] = field(default_factory=list)
    project: Optional[ProjectStatusData] = None
    repo_brief: Optional[RepoTechnicalBrief] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
