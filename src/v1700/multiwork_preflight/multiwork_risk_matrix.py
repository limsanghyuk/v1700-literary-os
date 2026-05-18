from __future__ import annotations

from typing import Any


def build_multiwork_risk_matrix() -> dict[str, Any]:
    risks = [
        {"risk": "memory_contamination", "severity": "critical", "mitigation": "ProjectIsolationManager + feature-only reports"},
        {"risk": "permission_contamination", "severity": "critical", "mitigation": "AuthorLicense edge required before access"},
        {"risk": "canon_contamination", "severity": "critical", "mitigation": "CanonConflictReport before shared-world absorption"},
        {"risk": "direct_v571_merge", "severity": "critical", "mitigation": "Stage127 blocks direct merge; Stage128 read-only adapter first"},
        {"risk": "gate_authority_drift", "severity": "high", "mitigation": "Gate25 primary + Gate28/29 secondary Governor compatibility check"},
    ]
    return {
        "status": "pass",
        "risk_count": len(risks),
        "critical_risks": [r for r in risks if r["severity"] == "critical"],
        "risks": risks,
    }
