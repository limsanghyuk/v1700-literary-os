from __future__ import annotations

from pathlib import Path

from v1700.gates.stage90_release_gate import run_stage90_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.writer_studio.event_replay import run_stage91_event_replay_smoke


_STAGE91_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage91_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE91_CACHE:
        return _STAGE91_CACHE[cache_key]

    stage90 = run_stage90_release_gate(root)
    replay = run_stage91_event_replay_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage90_release_gate": stage90,
        "stage91_event_replay_smoke": replay,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if replay.get("event_count", 0) < 18:
        issues.append("stage91_event_count_below_18")
    if replay.get("persistence_snapshot_count", 0) < 3:
        issues.append("stage91_persistence_snapshot_count_below_3")
    if replay.get("review_queue_total_items", 0) < 6:
        issues.append("stage91_review_queue_total_items_below_6")
    if replay.get("review_queue_blocking_count", 1) != 0:
        issues.append("stage91_blocking_reviews_unresolved")
    if replay.get("final_workspace_stage") != "91":
        issues.append("stage91_final_workspace_stage_not_91")
    if replay.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if replay.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")

    result = {
        "stage": "91",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage91 adds deterministic Writer Studio persistence, review queue state, and UI event replay on top of Stage90 round-trip export fidelity.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    _STAGE91_CACHE[cache_key] = result
    return result
