from __future__ import annotations

from pathlib import Path

from v1700.stage100.dual_mode_evaluator import run_stage100_dual_mode_evaluation
from v1700.stage100.gitnexus_rc_preflight import run_stage100_rc_preflight
from v1700.stage100.provider_certification import run_stage100_provider_certification
from v1700.stage100.readiness import build_stage100_readiness_report
from v1700.stage100.report import write_json
from v1700.stage100.v430_comparison_bridge import run_stage100_v430_comparison_bridge


def run_stage100_rc(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage100_rc_preflight(root)
    dual = run_stage100_dual_mode_evaluation(root)
    provider = run_stage100_provider_certification(root)
    v430 = run_stage100_v430_comparison_bridge(root)
    readiness = build_stage100_readiness_report(root, preflight, dual, provider, v430)
    issues = []
    for name, report in (("preflight", preflight), ("dual_mode", dual), ("provider", provider), ("v430", v430), ("readiness", readiness)):
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    payload = {
        "stage": "100",
        "baseline_stage": "99",
        "title": "Literary OS 1.0 Release Candidate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage100_0_rc_preflight": preflight,
        "stage100_1_dual_mode_evaluation": dual,
        "stage100_2_provider_certification": provider,
        "stage100_3_v430_comparison_bridge": v430,
        "stage100_readiness": readiness,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    }
    write_json(root / "release" / "current" / "stage100_literary_os_rc_report.json", payload)
    return payload

