from __future__ import annotations

from pathlib import Path

from v1700.gates.stage89_release_gate import run_stage89_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.writer_studio.roundtrip import run_stage90_roundtrip_smoke


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


_STAGE90_CACHE: dict[str, dict] = {}


def run_stage90_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE90_CACHE:
        return _STAGE90_CACHE[cache_key]

    stage89 = run_stage89_release_gate(root)
    roundtrip = run_stage90_roundtrip_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage89_release_gate": stage89,
        "stage90_roundtrip_smoke": roundtrip,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if roundtrip.get("applied_count", 0) < 4:
        issues.append("stage90_required_edit_count_below_4")
    if roundtrip.get("changed_artifact_count", 0) < 5:
        issues.append("stage90_export_artifacts_not_all_changed")
    if roundtrip.get("fidelity_score", 0) < 10.0:
        issues.append("stage90_fidelity_score_below_10")
    if roundtrip.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if roundtrip.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")

    result = {
        "stage": "90",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage90 hardens Writer Studio with deterministic round-trip editing and export fidelity checks on top of Stage89.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    _STAGE90_CACHE[cache_key] = result
    return result
