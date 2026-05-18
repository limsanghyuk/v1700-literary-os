from __future__ import annotations

from pathlib import Path

from v1700.gates.gitnexus_index_quality_gate import run_gitnexus_index_quality_gate
from v1700.gates.graph_nexus_release_gate import run_graph_nexus_release_gate
from v1700.gates.stage83_1_release_gate import run_stage83_1_release_gate
from v1700.gates.stage84_release_gate import run_stage84_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage85_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    stage83_1 = run_stage83_1_release_gate(root)
    stage84 = run_stage84_release_gate(root)
    graph_nexus = run_graph_nexus_release_gate(root)
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    index_quality = run_gitnexus_index_quality_gate(root)
    checks = {
        "stage83_1_release_gate": stage83_1,
        "stage84_release_gate": stage84,
        "graph_nexus_release_gate": graph_nexus,
        "symbol_to_branchpoint_trace_gate": trace_gate,
        "gitnexus_index_quality_gate": index_quality,
    }
    issues = [
        name
        for name, report in checks.items()
        if report.get("status") != "pass"
    ]
    if stage84.get("provider_default_calls") != 0 or index_quality.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if stage84.get("node2_raw_reveal_access_count") != 0 or index_quality.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "85",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage85 proves GitNexus density and symbol-to-branchpoint traceability without making GitNexus a mandatory runtime dependency.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }

