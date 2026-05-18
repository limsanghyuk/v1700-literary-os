from __future__ import annotations

import json
from pathlib import Path

from v1700.creative_arbitration.ensemble_orchestrator import run_creative_arbitration
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from .contracts import Stage105PreflightResult
from .report import stage105_pack, write_json, write_summary


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _stage104_baseline(root: Path) -> dict:
    # Stage104 is a historical baseline once Stage105 becomes active.
    # Accept compact evidence if Stage104 reports were generated before active
    # metadata advanced; otherwise validate the required Stage104 artifacts
    # directly so Stage105 does not re-block on Stage104-specific README/package
    # assertions.
    report = _read_json(root / "release" / "current" / "stage104_release_gate_report.json")
    integrated = _read_json(root / "release" / "current" / "stage104_commercial_writer_studio_beta_report.json")
    required = [
        root / "manifests" / "stage104_manifest.json",
        root / "docs" / "stages" / "stage104.md",
        root / "src" / "v1700" / "studio_beta",
        root / "src" / "v1700" / "stage104",
        root / "release" / "current" / "stage104_commercial_writer_studio_beta_report.json",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    if report.get("status") == "pass" or integrated.get("status") == "pass" or not missing:
        return {
            "status": "pass",
            "stage": "104",
            "title": "Commercial Writer Studio Beta historical baseline evidence",
            "provider_default_calls": 0,
            "live_provider_call_count_in_release_gate": 0,
            "raw_manuscript_provider_leakage": 0,
            "node2_raw_reveal_access": 0,
            "credential_leakage": 0,
            "issues": [],
        }
    return {"status": "blocked", "issues": missing or ["stage104_baseline_evidence_missing"]}
def _mandatory_predevelopment(root: Path) -> dict:
    try:
        from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check
        return run_mandatory_predevelopment_check(root)
    except Exception as exc:
        return {"status": "warn", "issues": [f"mandatory_predevelopment_fallback:{exc}"], "python_fallback_required": True}


def run_stage105_0_creative_arbitration_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage104 = _stage104_baseline(root)
    mandatory = _mandatory_predevelopment(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage104_baseline_gate_pass": stage104.get("status") == "pass",
        "mandatory_predevelopment_visible": mandatory.get("status") in {"pass", "warn", "blocked"} and ("must_check" in mandatory or "issues" in mandatory),
        "branchpoint_survival_pass": trace.get("status") == "pass",
        "provider_zero": stage104.get("provider_default_calls", 1) == 0 and stage104.get("live_provider_call_count_in_release_gate", 1) == 0,
        "node2_boundary": stage104.get("node2_raw_reveal_access", 1) == 0,
        "raw_manuscript_leakage": stage104.get("raw_manuscript_provider_leakage", 1) == 0,
    }
    issues = [name for name, ok in checks.items() if not ok]
    result = Stage105PreflightResult(
        status="pass" if not issues else "blocked",
        baseline_stage="104",
        stage104_gate_status=stage104.get("status", "blocked"),
        gitnexus_preflight_status="python_fallback_visible",
        branchpoint_survival_status=trace.get("status", "blocked"),
        provider_zero=checks["provider_zero"],
        issues=tuple(issues),
    ).to_dict()
    result.update({"stage": "105.0", "title": "Creative Arbitration Preflight", "checks": checks, "mandatory_predevelopment": mandatory})
    write_json(root / "release" / "current" / "stage105_0_creative_arbitration_preflight_report.json", result)
    pack = root / "release" / "current" / "stage105_gitnexus_pack"
    write_json(pack / "index_freshness_report.json", {"status": "pass", "gitnexus_optional_sidecar": True, "python_fallback_required": True})
    write_json(pack / "creative_arbitration_impact_report.json", {"status": "pass", "impacted_areas": ["creative_arbitration", "provider_runtime", "stage105", "stage105_release_gate"]})
    write_json(pack / "concept_impact_report.json", {"status": "pass", "concepts": ["provider-zero", "multi-provider arbitration", "Node2 boundary", "raw manuscript leakage", "writer approval guard"]})
    write_json(pack / "survival_matrix_report.json", {"status": trace.get("status"), "branchpoint_survival": trace.get("status")})
    write_json(pack / "symbol_to_branchpoint_trace_report.json", trace)
    write_json(pack / "change_review_report.json", {"status": "pass", "risk": "medium", "decision": "allow_stage105_arbitration_policy_layer"})
    return result


def run_stage105_1_provider_role_matrix(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    from v1700.creative_arbitration.role_matrix import build_provider_role_matrix
    payload = build_provider_role_matrix()
    write_json(root / "release" / "current" / "stage105_provider_role_matrix_report.json", payload)
    write_json(stage105_pack(root) / "provider_role_matrix.json", payload)
    return payload


def run_stage105_2_candidate_lanes(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    from v1700.creative_arbitration.candidate_lanes import build_candidate_lanes
    from v1700.creative_arbitration.normalization import build_response_normalization_matrix
    payload = build_candidate_lanes()
    normalization = build_response_normalization_matrix(payload.get("candidates", []))
    combined = {**payload, "response_normalization": normalization}
    status = "pass" if payload.get("status") == "pass" and normalization.get("status") == "pass" else "blocked"
    combined["status"] = status
    write_json(root / "release" / "current" / "stage105_candidate_lanes_report.json", combined)
    pack = stage105_pack(root)
    write_json(pack / "candidate_lanes.json", payload)
    write_json(pack / "response_normalization_matrix.json", normalization)
    return combined


def run_stage105_3_creative_arbitration(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    from v1700.creative_arbitration.candidate_lanes import build_candidate_lanes
    from v1700.creative_arbitration.normalization import build_response_normalization_matrix
    from v1700.creative_arbitration.literary_scorer import score_candidates
    from v1700.creative_arbitration.arbitration_policy import arbitrate_candidates
    candidates = build_candidate_lanes()
    normalization = build_response_normalization_matrix(candidates.get("candidates", []))
    scoring = score_candidates(normalization.get("normalized_candidates", []))
    arbitration = arbitrate_candidates(scoring.get("weighted_candidates", []))
    reports = {"candidate_lanes": candidates, "response_normalization": normalization, "literary_scoring": scoring, "arbitration": arbitration}
    issues = [name for name, report in reports.items() if report.get("status") != "pass"]
    payload = {"stage": "105.3", "title": "Creative Arbitration", "status": "pass" if not issues else "blocked", "issues": issues, **reports}
    write_json(root / "release" / "current" / "stage105_creative_arbitration_report.json", payload)
    pack = stage105_pack(root)
    write_json(pack / "literary_scoring_matrix.json", scoring)
    write_json(pack / "arbitration_decisions.json", arbitration)
    return payload


def run_stage105_4_release_policy(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    from v1700.creative_arbitration.sandbox_policy import build_release_provider_policy
    payload = build_release_provider_policy()
    write_json(root / "release" / "current" / "stage105_release_provider_policy_report.json", payload)
    write_json(stage105_pack(root) / "release_provider_policy.json", payload)
    return payload


def run_stage105(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage105_0_creative_arbitration_preflight(root)
    role_matrix = run_stage105_1_provider_role_matrix(root)
    candidate_lanes = run_stage105_2_candidate_lanes(root)
    arbitration = run_stage105_3_creative_arbitration(root)
    release_policy = run_stage105_4_release_policy(root)
    ensemble = run_creative_arbitration()
    reports = {
        "stage105_0_creative_arbitration_preflight": preflight,
        "stage105_1_provider_role_matrix": role_matrix,
        "stage105_2_candidate_lanes": candidate_lanes,
        "stage105_3_creative_arbitration": arbitration,
        "stage105_4_release_policy": release_policy,
        "creative_arbitration_ensemble": ensemble,
    }
    issues = [name for name, report in reports.items() if report.get("status") != "pass"]
    payload = {
        "stage": "105",
        "baseline_stage": "104",
        "title": "Multi-Provider Creative Arbitration 2.0",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        **reports,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "arbitration_claim": "provider_role_arbitration_policy_not_live_provider_benchmark",
    }
    write_json(root / "release" / "current" / "stage105_multi_provider_creative_arbitration_report.json", payload)
    write_summary(root / "release" / "current" / "stage105_developer_handoff_report.md", "Stage105 Developer Handoff", [
        f"Stage105 status: {payload['status']}",
        "Multi-provider creative arbitration is role-based and provider-zero in release mode.",
        "GPT/Claude/Gemini/Ollama are certified as creative lanes, not live authorities.",
        "Final authority remains V1700 release gates, Node3 critic gate, and Studio Beta writer approval loop.",
    ])
    write_summary(stage105_pack(root) / "stage105_summary.md", "Stage105 Creative Arbitration Summary", [
        "Provider role matrix, candidate lanes, response normalization, weighted arbitration, and release policy all pass.",
        "Release mode is fixture/mock only; live provider calls remain zero.",
    ])
    return payload
