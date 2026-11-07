"""Data models for business and strategic analysis outputs."""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class VerifiedKPI:
    """A mathematically verified performance indicator with traceable origin."""
    key: str
    label: str
    value_display: str
    numeric_value: float
    target_value: float
    variance_pct: float
    status: str  # ON_TARGET, EXCEEDED, AT_RISK, OFF_TRACK
    provenance_source: str  # e.g., 'financials.2026-Q4.revenue_actual'
    confidence: float = 1.0


@dataclass
class BusinessAnalysisOutput:
    """Comprehensive outputs from the Business Analyst Agent."""
    period_label: str
    summary_headline: str
    kpis: List[VerifiedKPI] = field(default_factory=list)
    growth_trends: Dict[str, float] = field(default_factory=dict)
    operational_health_score: float = 0.0  # 0 - 100
    financial_runway_assessment: str = ""
    calculated_flags: List[str] = field(default_factory=list)


@dataclass
class StrategicPillar:
    """A strategic priority aligned with executive decision-making."""
    title: str
    rationale: str
    action_items: List[str] = field(default_factory=list)
    impact_level: str = "HIGH"  # CRITICAL, HIGH, MEDIUM


@dataclass
class StrategyConsultantOutput:
    """Structured narrative formulated by the Strategy Consultant Agent."""
    executive_thesis: str
    situation: str
    complication: str
    resolution_strategy: str
    strategic_pillars: List[StrategicPillar] = field(default_factory=list)
    board_recommendations: List[str] = field(default_factory=list)
    required_decisions: List[str] = field(default_factory=list)
