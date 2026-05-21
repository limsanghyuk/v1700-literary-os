from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage138_release_gate import run_stage138_release_gate
from v1700.stage139 import run_stage139

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage139_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = _baseline_gate(root)
    stage = run_stage139(root)
    pipeline = stage.get("parts", {}).get("corpus_governance_pipeline", {})
    total_items = int(stage.get("total_pipeline_items", 0))
    checks = {
        "stage138_baseline_gate_pass": _check(
            baseline.get("status") == "pass" or baseline.get("stage138", {}).get("status") == "pass"
        ),
        "corpus_governance_report_pass": _check(stage.get("status") == "pass"),
        "corpus_governance_pipeline_pass": _check(pipeline.get("status") == "pass"),
        "governance_mode_pass": _check(
            stage.get("corpus_governance_pipeline_only") is True
            and stage.get("mode") == "CORPUS_GOVERNANCE_PIPELINE_DRY_RUN"
        ),
        "governance_profiles_present": _check(stage.get("governance_profile_count", 0) >= 3),
        "governed_case_coverage_pass": _check(
            stage.get("governed_case_count") == stage.get("case_packet_count")
            and stage.get("policy_binding_count") == stage.get("case_packet_count")
            and stage.get("governed_case_count", 0) >= 1
        ),
        "review_queue_preserved_pass": _check(
            stage.get("review_queue_packet_count", 0) >= 1 and stage.get("review_required_case_count", 0) >= 1
        ),
        "retention_metadata_pass": _check(stage.get("retention_ready_count") == stage.get("case_packet_count")),
        "audit_trail_ready_pass": _check(stage.get("audit_trail_ready_count") == total_items),
        "stage140_release_ready_pass": _check(stage.get("stage140_release_ready_count") == total_items),
        "rollback_ready_metadata_pass": _check(stage.get("rollback_ready_count") == total_items),
        "unique_profile_pass": _check(stage.get("unique_profile_count") == stage.get("governance_profile_count")),
        "governance_execution_blocked": _check(
            stage.get("losdb_write_enabled") is False
            and stage.get("storage_contract_write_enabled") is False
            and stage.get("execution_blocked_count") == total_items
        ),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(
            stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0
        ),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(
            stage.get("raw_manuscript_provider_leakage") == 0
            and stage.get("raw_manuscript_cross_project_leakage") == 0
        ),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "139",
        "baseline_stage": "138",
        "title": "Corpus Governance Pipeline Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage139": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage139_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage139":
        report = _load_report(root, "stage138_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage138_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_report(root: Path, name: str) -> dict[str, Any] | None:
    path = root / "release" / "current" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "corpus_governance_pipeline_only",
        "governance_profile_count",
        "case_packet_count",
        "review_queue_packet_count",
        "governed_case_count",
        "review_required_case_count",
        "retention_ready_count",
        "audit_trail_ready_count",
        "stage140_release_ready_count",
        "execution_blocked_count",
        "rollback_ready_count",
        "policy_binding_count",
        "unique_profile_count",
        "total_pipeline_items",
        "losdb_write_enabled",
        "migration_execution_enabled",
        "storage_contract_write_enabled",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage",
        "credential_leakage",
        "cross_project_write_allowed",
        "canon_auto_resolution_count",
        "auto_repair_mutation_count",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage139.md",
            "docs/proposals/stage139_proposal.md",
            "docs/architecture/stage139_blueprint.md",
            "docs/development/stage139_developer_handoff.md",
            "manifests/stage139_manifest.json",
            "manifests/stage139_corpus_governance_pipeline_manifest.json",
            "manifests/stage139_branchpoint_trace_manifest.json",
            "manifests/live_core_stage139_overlay.json",
            "release/current/stage139_corpus_governance_pipeline_report.json",
            "release/current/stage139_corpus_governance_pipeline_pack/governance_pipeline.json",
            "release/current/stage139_corpus_governance_pipeline_pack/stage139_preflight_report.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [
        root / ".github/workflows/ci-core.yml",
        root / ".github/workflows/cd-dry-run.yml",
        root / ".github/workflows/release.yml",
        root / "RELEASE_NOTES.md",
        root / "package_manifest.json",
    ]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(
        token in contents
        for token in [
            "stage139",
            "run_stage139_corpus_governance_pipeline.py",
            "run_stage139_release_gate.py",
        ]
    )
