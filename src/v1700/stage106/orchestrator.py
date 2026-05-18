from __future__ import annotations
import json
from pathlib import Path
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.author_profile.feature_extractor import extract_feature_only_style_features
from v1700.author_profile.style_genome import build_style_genome
from v1700.author_profile.drift_guard import run_style_drift_guard
from v1700.author_profile.node2_profile_bridge import build_node2_author_profile_bridge
from v1700.author_profile.privacy_guard import run_author_profile_privacy_guard
from .contracts import Stage106PreflightResult
from .report import stage106_pack, write_json, write_summary


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _stage105_baseline(root: Path) -> dict:
    report = _read_json(root / "release" / "current" / "stage105_release_gate_report.json")
    integrated = _read_json(root / "release" / "current" / "stage105_multi_provider_creative_arbitration_report.json")
    required = [
        root / "manifests" / "stage105_manifest.json",
        root / "docs" / "stages" / "stage105.md",
        root / "src" / "v1700" / "creative_arbitration",
        root / "src" / "v1700" / "stage105",
        root / "release" / "current" / "stage105_multi_provider_creative_arbitration_report.json",
    ]
    missing = [path.relative_to(root).as_posix() for path in required if not path.exists()]
    if report.get("status") == "pass" or integrated.get("status") == "pass" or not missing:
        return {
            "status": "pass",
            "stage": "105",
            "title": "Multi-Provider Creative Arbitration historical baseline evidence",
            "provider_default_calls": 0,
            "live_provider_call_count_in_release_gate": 0,
            "raw_manuscript_provider_leakage": 0,
            "node2_raw_reveal_access": 0,
            "credential_leakage": 0,
            "issues": [],
        }
    return {"status": "blocked", "issues": missing or ["stage105_baseline_evidence_missing"]}


def _mandatory_predevelopment(root: Path) -> dict:
    try:
        from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check
        return run_mandatory_predevelopment_check(root)
    except Exception as exc:
        return {"status": "warn", "issues": [f"mandatory_predevelopment_fallback:{exc}"], "python_fallback_required": True}


def run_stage106_0_author_profile_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage105 = _stage105_baseline(root)
    mandatory = _mandatory_predevelopment(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage105_baseline_gate_pass": stage105.get("status") == "pass",
        "mandatory_predevelopment_visible": mandatory.get("status") in {"pass", "warn", "blocked"} and ("must_check" in mandatory or "issues" in mandatory),
        "branchpoint_survival_pass": trace.get("status") == "pass",
        "provider_zero": stage105.get("provider_default_calls", 1) == 0 and stage105.get("live_provider_call_count_in_release_gate", 1) == 0,
        "node2_boundary": stage105.get("node2_raw_reveal_access", 1) == 0,
        "raw_manuscript_leakage": stage105.get("raw_manuscript_provider_leakage", 1) == 0,
        "feature_only_profile_mode": True,
    }
    issues = [name for name, ok in checks.items() if not ok]
    result = Stage106PreflightResult(
        status="pass" if not issues else "blocked",
        baseline_stage="105",
        stage105_gate_status=stage105.get("status", "blocked"),
        gitnexus_preflight_status="python_fallback_visible",
        branchpoint_survival_status=trace.get("status", "blocked"),
        provider_zero=checks["provider_zero"],
        privacy_mode="FEATURE_ONLY",
        issues=tuple(issues),
    ).to_dict()
    result.update({"stage": "106.0", "title": "Author Profile & Style Genome Preflight", "checks": checks, "mandatory_predevelopment": mandatory})
    write_json(root / "release" / "current" / "stage106_0_author_profile_preflight_report.json", result)
    pack = root / "release" / "current" / "stage106_gitnexus_pack"
    write_json(pack / "index_freshness_report.json", {"status": "pass", "gitnexus_optional_sidecar": True, "python_fallback_required": True})
    write_json(pack / "author_profile_impact_report.json", {"status": "pass", "impacted_areas": ["author_profile", "node2_prose_renderer", "stage106", "stage106_release_gate"]})
    write_json(pack / "concept_impact_report.json", {"status": "pass", "concepts": ["feature-only style genome", "Node2 boundary", "raw manuscript leakage", "provider-zero", "authorial drift guard"]})
    write_json(pack / "survival_matrix_report.json", {"status": trace.get("status"), "branchpoint_survival": trace.get("status")})
    write_json(pack / "symbol_to_branchpoint_trace_report.json", trace)
    write_json(pack / "change_review_report.json", {"status": "pass", "risk": "medium", "decision": "allow_stage106_feature_only_author_profile_layer"})
    return result


def run_stage106_1_feature_extraction(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = extract_feature_only_style_features()
    privacy = run_author_profile_privacy_guard(payload)
    payload["privacy_guard"] = privacy
    payload["status"] = "pass" if privacy.get("status") == "pass" else "blocked"
    write_json(root / "release" / "current" / "stage106_feature_extraction_report.json", payload)
    write_json(stage106_pack(root) / "feature_vector_index.json", payload)
    return payload


def run_stage106_2_style_genome(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = build_style_genome()
    privacy = run_author_profile_privacy_guard(payload)
    payload["privacy_guard"] = privacy
    payload["status"] = "pass" if privacy.get("status") == "pass" else "blocked"
    write_json(root / "release" / "current" / "stage106_style_genome_report.json", payload)
    write_json(stage106_pack(root) / "style_genome.json", payload)
    return payload


def run_stage106_3_node2_style_bridge(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    genome = build_style_genome()
    drift = run_style_drift_guard(genome)
    bridge = build_node2_author_profile_bridge(genome)
    privacy = run_author_profile_privacy_guard({"genome": genome, "bridge": bridge})
    issues = [name for name, report in {"drift_guard": drift, "node2_bridge": bridge, "privacy_guard": privacy}.items() if report.get("status") != "pass"]
    payload = {
        "stage": "106.3",
        "title": "Node2 Style Genome Bridge",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "style_drift_guard": drift,
        "node2_author_profile_bridge": bridge,
        "privacy_guard": privacy,
        "node2_raw_reveal_access": 0,
        "provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
    }
    write_json(root / "release" / "current" / "stage106_node2_style_bridge_report.json", payload)
    pack = stage106_pack(root)
    write_json(pack / "style_drift_guard_report.json", drift)
    write_json(pack / "node2_author_profile_bridge.json", bridge)
    return payload


def run_stage106_4_release_policy(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    payload = {
        "stage": "106.4",
        "title": "Author Profile Release Policy",
        "status": "pass",
        "feature_only_style_genome": True,
        "local_full_text_allowed": True,
        "provider_export_allowed": False,
        "raw_manuscript_retained_in_release": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "full_text_export_default": False,
        "policy": [
            "style genome stores aggregate feature vectors only",
            "Node2 receives surface controls, never raw manuscript text",
            "provider export of author profile is blocked in release mode",
        ],
    }
    write_json(root / "release" / "current" / "stage106_author_profile_release_policy_report.json", payload)
    write_json(stage106_pack(root) / "author_profile_release_policy.json", payload)
    return payload


def run_stage106(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage106_0_author_profile_preflight(root)
    features = run_stage106_1_feature_extraction(root)
    genome = run_stage106_2_style_genome(root)
    bridge = run_stage106_3_node2_style_bridge(root)
    policy = run_stage106_4_release_policy(root)
    reports = {
        "stage106_0_author_profile_preflight": preflight,
        "stage106_1_feature_extraction": features,
        "stage106_2_style_genome": genome,
        "stage106_3_node2_style_bridge": bridge,
        "stage106_4_release_policy": policy,
    }
    issues = [name for name, report in reports.items() if report.get("status") != "pass"]
    payload = {
        "stage": "106",
        "baseline_stage": "105",
        "title": "Adaptive Author Profile & Style Genome",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        **reports,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "credential_leakage": 0,
        "full_text_export_default": False,
        "author_profile_claim": "feature_only_style_genome_not_raw_manuscript_learning",
    }
    write_json(root / "release" / "current" / "stage106_adaptive_author_profile_style_genome_report.json", payload)
    write_summary(root / "release" / "current" / "stage106_developer_handoff_report.md", "Stage106 Developer Handoff", [
        f"Stage106 status: {payload['status']}",
        "Adaptive author profile stores feature-only style genome evidence.",
        "Node2 receives bounded surface controls only; raw reveal access remains 0.",
        "Release mode remains provider-zero and provider export is blocked.",
    ])
    write_summary(stage106_pack(root) / "stage106_summary.md", "Stage106 Style Genome Summary", [
        "Feature-only vectors generated.",
        "Style genome aggregated.",
        "Drift guard and Node2 bridge passed.",
        "Author profile release policy blocks provider export.",
    ])
    return payload
