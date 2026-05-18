from __future__ import annotations
from pathlib import Path
from v1700.gates.stage76_release_gate import run_stage76_release_gate
from v1700.nodes.node2_prose_renderer.rewrite_orchestrator import run_node2_rewrite_restoration_smoke


def run_stage77_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage76 = run_stage76_release_gate(root)
    node2 = run_node2_rewrite_restoration_smoke()
    issues: list[str] = []
    if stage76.get("status") != "pass":
        issues.append("stage76_release_gate_blocked")
    if node2.get("status") != "pass":
        issues.append("node2_rewrite_restoration_blocked")
    return {"stage": "77", "status": "pass" if not issues else "blocked", "issues": issues, "stage76_release_gate": stage76, "node2_rewrite_restoration": node2, "provider_default_calls": 0, "node2_raw_reveal_access_count": 0}
