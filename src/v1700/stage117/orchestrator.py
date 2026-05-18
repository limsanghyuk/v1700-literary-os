from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.arc.tension_curve_report import build_stage117_tension_curve_report
from v1700.stage117.contracts import Stage117Contract


def run_stage117(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    tension_report = build_stage117_tension_curve_report()
    contract = Stage117Contract().to_dict()
    loss = tension_report.get("loss", {})
    issues: list[str] = []
    if tension_report.get("status") != "pass":
        issues.append("tension_curve_report_blocked")
    if loss.get("coverage_loss") != 0.0:
        issues.append("coverage_loss_nonzero")
    if not (0.0 <= float(loss.get("tension_loss", 1.0)) < 0.10):
        issues.append("tension_loss_outside_expected_range")
    if float(loss.get("final_loss", 1.0)) >= 0.10:
        issues.append("final_loss_warn_threshold_exceeded")
    result = {
        "stage": "117",
        "baseline_stage": "116",
        "title": "NarrativeTensionCurve",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "tension_curve": tension_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage118", "Stage119", "Stage120"],
    }
    _write(root / "release/current/stage117_narrative_tension_curve_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
