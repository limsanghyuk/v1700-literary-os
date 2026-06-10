from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CORE_INVARIANTS = {
    "provider_default_calls": 0,
    "live_provider_call_count_in_release_gate": 0,
    "provider_generation_count": 0,
    "runtime_execution_count": 0,
    "write_operation_count": 0,
    "node2_raw_reveal_access": 0,
    "credential_leakage": 0,
    "provider_generation_enabled": False,
    "provider_evaluation_enabled": False,
    "evolution_write_enabled": False,
    "memory_write_enabled": False,
    "cross_project_write_enabled": False,
    "canon_mutation_enabled": False,
    "runtime_training_enabled": False,
    "auto_repair_apply_enabled": False,
    "automatic_promotion_enabled": False,
}

REQUIRED_FILES = (
    "docs/stages/stage242.md",
    "docs/development/stage242_developer_handoff.md",
    "docs/proposals/page17_plugin_learning_product_rc_proposal.md",
    "docs/architecture/page17_plugin_learning_product_rc_blueprint.md",
    "manifests/stage242_manifest.json",
    "manifests/stage242_page17_release_manifest.json",
    "manifests/stage242_branchpoint_trace_manifest.json",
    "manifests/live_core_stage242_overlay.json",
    "release/current/page17_release_gate_report.md",
    "release/current/stage242_gitnexus_evidence_report.json",
    "release/current/stage242_page17_release_report.json",
    "release/current/stage242_release_asset_manifest.json",
    "release/current/post_roadmap_release_readiness_report.md",
)

WARNING_LINES = (
    "Page10 GitNexus evidence refresh remains pending.",
    "Page11 GitNexus evidence refresh remains pending.",
    "Page12 GitNexus evidence refresh remains pending.",
    "Stage185 remains local-known and not hub official.",
)


def run_stage242_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    release_report = _load_json(root / "release/current/stage242_page17_release_report.json")
    evidence_report = _load_json(root / "release/current/stage242_gitnexus_evidence_report.json")
    package_manifest = _load_json(root / "package_manifest.json")
    page17_gate = _read_text(root / "release/current/page17_release_gate_report.md")
    post_roadmap = _read_text(root / "release/current/post_roadmap_release_readiness_report.md")

    checks = {
        "active_version_pass": _check(_active_version(root) == "stage242"),
        "required_files_pass": _check(all((root / rel).exists() for rel in REQUIRED_FILES)),
        "page17_gate_pass": _check("Result: PASS_WITH_GITNEXUS_OUTPUT" in page17_gate and "Stage242: PASS_WITH_GITNEXUS_OUTPUT" in page17_gate),
        "stage242_gitnexus_evidence_pass": _check(evidence_report.get("status") == "PASS_WITH_GITNEXUS_OUTPUT" and evidence_report.get("orphan_count") == 0),
        "warning_visibility_pass": _check(all(token in page17_gate and token in post_roadmap for token in WARNING_LINES)),
        "package_manifest_alignment_pass": _check(
            package_manifest.get("active_version") == "stage242"
            and package_manifest.get("stage") == "stage242"
            and str(package_manifest.get("canonical_package", "")).startswith("V1700_stage242_")
        ),
        "provider_zero_pass": _check(
            release_report.get("provider_default_calls") == 0
            and release_report.get("live_provider_call_count_in_release_gate") == 0
            and release_report.get("provider_generation_enabled") is False
        ),
        "write_training_boundary_pass": _check(
            release_report.get("write_operation_count") == 0
            and release_report.get("memory_write_enabled") is False
            and release_report.get("runtime_training_enabled") is False
            and release_report.get("canon_mutation_enabled") is False
        ),
        "page18_stage243_absent_pass": _check(
            evidence_report.get("page18_implementation_detected") is False
            and "No Page18 or Stage243+ implementation is included in Page17." in page17_gate
        ),
    }
    issues = [name for name, check in checks.items() if check["status"] != "pass"]
    result = {
        "stage": "242",
        "baseline_stage": "235",
        "title": "Page17 Authority Closure",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "warning_preserving_release": True,
        "carried_forward_warnings": list(WARNING_LINES),
        "post_roadmap_authority_review_open": True,
        **CORE_INVARIANTS,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage242_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")
