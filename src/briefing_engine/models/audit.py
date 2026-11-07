"""Data models for fact-checking, quality assurance, and audit trails."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class AuditSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class AuditFinding:
    """An individual assertion verification finding."""
    claim_text: str
    card_id: str
    is_verified: bool
    source_reference: Optional[str] = None
    finding_type: str = "VERIFIED"  # VERIFIED, UNVERIFIED_CLAIM, DATA_DISCREPANCY, HALLUCINATION_FLAG
    severity: AuditSeverity = AuditSeverity.INFO
    explanation: str = ""


@dataclass
class AuditReport:
    """Overall quality and mathematical integrity audit report."""
    total_claims_audited: int
    verified_claims_count: int
    unverified_claims_count: int
    data_gaps_identified: List[str] = field(default_factory=list)
    findings: List[AuditFinding] = field(default_factory=list)
    passed_audit_gate: bool = True
    audit_score_pct: float = 100.0

    def summary_status(self) -> str:
        if self.passed_audit_gate and self.audit_score_pct >= 90:
            return "PASSED (Enterprise Grade)"
        elif self.passed_audit_gate:
            return "PASSED WITH WARNINGS"
        return "FAILED AUDIT GATE"
