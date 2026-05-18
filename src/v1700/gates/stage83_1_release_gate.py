
from __future__ import annotations

from pathlib import Path

from v1700.lineage.stage83_1_consistency_audit import run_stage83_1_consistency_audit


def run_stage83_1_release_gate(root: Path | None = None) -> dict:
    audit = run_stage83_1_consistency_audit(root)
    issues: list[str] = []
    if audit.get("status") != "pass":
        issues.append("stage83_1_consistency_audit_blocked")
    if audit.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if audit.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "83.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage83.1 release gate passes only after branchpoint/core-logic/organic-relation/commercial-gap manifests are reconciled through Stage83.",
        "consistency_audit": audit,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
