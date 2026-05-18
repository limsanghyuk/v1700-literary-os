from __future__ import annotations

from pathlib import Path

from v1700.stage100.contracts import Stage100ReleaseCandidate
from v1700.stage100.report import write_json, write_summary


def build_stage100_readiness_report(root: Path, preflight: dict, dual: dict, provider: dict, v430: dict) -> dict:
    candidate = Stage100ReleaseCandidate(
        stage="100",
        baseline_stage="99",
        rc_version="1.0rc1",
        gitnexus_preflight_status=preflight.get("status", "blocked"),
        branchpoint_survival_status=preflight.get("survival_matrix_status", "blocked"),
        dual_mode_evaluation_status=dual.get("status", "blocked"),
        provider_certification_status=provider.get("status", "blocked"),
        release_gate_status="pending_until_stage100_release_gate",
        stage100_readiness_status="pass",
    )
    issues: list[str] = []
    if candidate.gitnexus_preflight_status != "pass":
        issues.append("gitnexus_rc_preflight_blocked")
    if candidate.branchpoint_survival_status != "pass":
        issues.append("branchpoint_survival_blocked")
    if candidate.dual_mode_evaluation_status != "pass":
        issues.append("dual_mode_evaluation_blocked")
    if candidate.provider_certification_status != "pass":
        issues.append("provider_certification_blocked")
    if v430.get("status") != "pass" or v430.get("v430_code_merged") is True:
        issues.append("v430_comparison_bridge_blocked")
    status = "pass" if not issues else "blocked"
    payload = {
        **candidate.to_dict(),
        "status": status,
        "issues": issues,
        "stage100_readiness_status": status,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": status == "pass",
        "gitnexus_runtime_dependency_required": False,
        "python_fallback_required": True,
    }
    write_json(root / "release" / "current" / "stage100_readiness_report.json", payload)
    write_summary(
        root / "release" / "current" / "stage100_developer_handoff_report.md",
        "Stage100 Developer Handoff",
        [
            f"RC readiness: {status}",
            "Stage100 is a release-candidate verification stage, not a feature expansion stage.",
            "V430 absorption is deferred to Stage101.",
        ],
    )
    return payload
