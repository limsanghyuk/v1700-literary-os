from __future__ import annotations
from pathlib import Path

from v1700.gates.stage81_release_gate import run_stage81_release_gate
from v1700.lineage.reabsorption_reconciliation import run_reabsorption_reconciliation


def run_stage81_1_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage81 = run_stage81_release_gate(root)
    reconciliation = run_reabsorption_reconciliation()
    issues: list[str] = []
    if stage81.get("status") != "pass":
        issues.append("stage81_release_gate_blocked")
    if reconciliation.get("status") != "pass":
        issues.append("reabsorption_reconciliation_blocked")
    completion = reconciliation.get("reabsorption_completion_manifest", {})
    return {
        "stage": "81.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage81.1 reconciles Stage75 missing/partial P0 branchpoint logic after Stage76~81 reabsorption.",
        "stage81_release_gate": stage81,
        "reabsorption_reconciliation": reconciliation,
        "p0_live_runtime_count": completion.get("p0_live_runtime_count", 0),
        "p0_partial_count": completion.get("p0_partial_count", 0),
        "p0_missing_count": completion.get("p0_missing_count", 0),
        "commercial_readiness_gap_count": len(reconciliation.get("commercial_readiness_gap_manifest", {}).get("items", [])),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
