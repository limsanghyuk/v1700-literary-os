from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage145_release_gate import run_stage145_release_gate
from v1700.gates.stage146_release_gate import run_stage146_release_gate
from v1700.gates.stage147_release_gate import run_stage147_release_gate
from v1700.gates.stage148_release_gate import run_stage148_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency
from v1700.stage148 import run_stage148

from .contracts import ConstitutionGateRule, LineageEvidence, ReleaseBlocker, StageReadinessCheck

TARGET_STAGE = "stage149"
TARGET_REPORT = "release/current/stage149_body_constitution_release_gate_report.json"


def run_stage149_body_constitution_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage149_body_constitution_release_gate_pack"
    pack.mkdir(parents=True, exist_ok=True)
    report_path = root / TARGET_REPORT
    if not report_path.exists():
        _write_json(
            report_path,
            {
                "stage": "149",
                "baseline_stage": "148",
                "title": "Body Constitution Release Gate",
                "status": "building",
                "issues": [],
            },
        )

    baseline = run_stage148_release_gate(root)
    stage145 = run_stage145_release_gate(root)
    stage146 = run_stage146_release_gate(root)
    stage147 = run_stage147_release_gate(root)
    stage148 = run_stage148(root)
    _write_json(root / "release/current/stage149_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    gate_matrix = _build_gate_matrix(stage145, stage146, stage147, baseline, stage148)
    constitution_seal = _build_page01_constitution_seal(root, gate_matrix, stage148)
    stage150_readiness = _build_stage150_readiness_matrix(root, constitution_seal, gate_matrix)
    blocker_registry = _build_release_blocker_registry(stage145, stage146, stage147, stage148)
    lineage_evidence = _build_lineage_evidence_index(root)

    _write_json(pack / "body_constitution_gate_matrix.json", gate_matrix)
    _write_json(pack / "page01_constitution_seal.json", constitution_seal)
    _write_json(pack / "stage150_readiness_matrix.json", stage150_readiness)
    _write_json(pack / "release_blocker_registry.json", blocker_registry)
    _write_json(pack / "lineage_evidence_index.json", lineage_evidence)

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage148_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "body_constitution_gate_matrix": gate_matrix,
        "page01_constitution_seal": constitution_seal,
        "stage150_readiness_matrix": stage150_readiness,
        "release_blocker_registry": blocker_registry,
        "lineage_evidence_index": lineage_evidence,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "149",
        "baseline_stage": "148",
        "title": "Body Constitution Release Gate",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "BODY_CONSTITUTION_RELEASE_GATE_LOCAL",
        "body_constitution_release_gate_only": True,
        "gate_rule_count": gate_matrix.get("rule_count", 0),
        "sealed_page01": constitution_seal.get("sealed_page01", False),
        "page01_constitution_frozen": constitution_seal.get("page01_constitution_frozen", False),
        "stage150_memory_body_ready": stage150_readiness.get("stage150_memory_body_ready", False),
        "release_blocker_count": blocker_registry.get("registered_blocker_count", 0),
        "blocked_capability_count": blocker_registry.get("blocked_capability_count", 0),
        "lineage_evidence_complete": lineage_evidence.get("coverage_complete", False),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage148_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "body_constitution_gate_matrix": gate_matrix,
            "page01_constitution_seal": constitution_seal,
            "stage150_readiness_matrix": stage150_readiness,
            "release_blocker_registry": blocker_registry,
            "lineage_evidence_index": lineage_evidence,
        },
    }
    _write_json(report_path, result)
    return result


def _build_gate_matrix(
    stage145: dict[str, Any],
    stage146: dict[str, Any],
    stage147: dict[str, Any],
    stage148_gate: dict[str, Any],
    stage148: dict[str, Any],
) -> dict[str, Any]:
    rules = (
        ConstitutionGateRule(
            "stage145_constitution_gate_pass",
            "Stage145 body constitution must remain the constitutional root of Page01.",
            stage145.get("status") == "pass",
            "stage145",
            "release/current/stage145_release_gate_report.json",
        ),
        ConstitutionGateRule(
            "stage146_state_contract_gate_pass",
            "Stage146 narrative state contract must remain canonical and passing.",
            stage146.get("status") == "pass",
            "stage146",
            "release/current/stage146_release_gate_report.json",
        ),
        ConstitutionGateRule(
            "stage147_manifest_body_gate_pass",
            "Stage147 manifest body must remain the bound packet authority.",
            stage147.get("status") == "pass",
            "stage147",
            "release/current/stage147_release_gate_report.json",
        ),
        ConstitutionGateRule(
            "stage148_node_boundary_gate_pass",
            "Stage148 node boundary constitution must remain the immediate baseline.",
            stage148_gate.get("status") == "pass",
            "stage148",
            "release/current/stage148_release_gate_report.json",
        ),
        ConstitutionGateRule(
            "stage148_entry_signal_pass",
            "Stage148 must explicitly declare Stage149 gate readiness.",
            stage148.get("stage149_gate_ready") is True,
            "stage148",
            "release/current/stage148_node_boundary_constitution_pack/stage149_entry_signals.json",
        ),
        ConstitutionGateRule(
            "provider_zero_preserved",
            "Page01 sealing must preserve provider-zero across the constitution chain.",
            all(report.get("provider_default_calls") == 0 for report in (stage145, stage146, stage147, stage148)),
            "stage145-stage148",
            "release/current/stage145_body_constitution_report.json",
        ),
        ConstitutionGateRule(
            "node2_boundary_preserved",
            "Page01 sealing must preserve Node2 raw reveal access = 0.",
            all(report.get("node2_raw_reveal_access") == 0 for report in (stage145, stage146, stage147, stage148)),
            "stage145-stage148",
            "release/current/stage148_node_boundary_constitution_report.json",
        ),
        ConstitutionGateRule(
            "branchpoint_lineage_preserved",
            "All Page01 stages must preserve branchpoint lineage evidence.",
            all(report.get("branchpoint_lineage_preserved") is True for report in (stage145, stage146, stage147, stage148)),
            "stage145-stage148",
            "manifests/stage149_branchpoint_trace_manifest.json",
        ),
    )
    issues = [rule.name for rule in rules if not rule.passed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage149 Body Constitution Gate Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "all_rules_passed": not issues,
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_page01_constitution_seal(
    root: Path,
    gate_matrix: dict[str, Any],
    stage148: dict[str, Any],
) -> dict[str, Any]:
    criteria_path = root / "release/current/stage145_body_constitution_pack/stage150_entry_criteria.json"
    criteria = _load_existing(criteria_path) or {}
    criterion_names = [entry.get("name") for entry in criteria.get("entries", [])]
    ready = (
        gate_matrix.get("status") == "pass"
        and stage148.get("stage149_gate_ready") is True
        and "stage149_release_gate_pass" in criterion_names
    )
    return {
        "stage": TARGET_STAGE,
        "title": "Stage149 Page01 Constitution Seal",
        "status": "pass" if ready else "blocked",
        "issues": [] if ready else ["page01_gate_matrix_or_entry_criteria_blocked"],
        "sealed_page01": ready,
        "page01_constitution_frozen": ready,
        "seal_status": "SEALED" if ready else "OPEN",
        "seal_authority": "Stage149 release gate",
        "seal_inputs": [
            "release/current/stage145_body_constitution_pack/stage150_entry_criteria.json",
            "release/current/stage148_node_boundary_constitution_pack/stage149_entry_signals.json",
            "release/current/stage149_body_constitution_release_gate_pack/body_constitution_gate_matrix.json",
        ],
        "next_stage": "stage150",
        "signals": [
            "Page01 constitutional layers Stage145 through Stage148 are passing and sealed.",
            "Stage150 Memory Body may begin only from this sealed constitution baseline.",
            "No provider calls, write paths, or raw reveal access are enabled by the seal.",
        ],
    }


def _build_stage150_readiness_matrix(
    root: Path,
    constitution_seal: dict[str, Any],
    gate_matrix: dict[str, Any],
) -> dict[str, Any]:
    criteria = _load_existing(root / "release/current/stage145_body_constitution_pack/stage150_entry_criteria.json") or {}
    gate_rule_names = {rule.get("name"): rule.get("passed") for rule in gate_matrix.get("rules", [])}
    checks = (
        StageReadinessCheck(
            "stage145_149_constitution_chain_pass",
            "The full Page01 constitution chain must pass before Stage150 starts.",
            gate_matrix.get("status") == "pass",
            "stage145-stage149",
        ),
        StageReadinessCheck(
            "page01_seal_present",
            "Stage149 must seal Page01 before Memory Body may start.",
            constitution_seal.get("sealed_page01") is True,
            "stage149",
        ),
        StageReadinessCheck(
            "stage149_entry_required_by_stage145",
            "Stage145 entry criteria must still explicitly require the Stage149 release gate.",
            any(entry.get("name") == "stage149_release_gate_pass" for entry in criteria.get("entries", [])),
            "stage145",
        ),
        StageReadinessCheck(
            "provider_zero_preserved",
            "Stage150 must inherit provider-zero from the sealed Page01 chain.",
            gate_rule_names.get("provider_zero_preserved") is True,
            "stage145-stage149",
        ),
        StageReadinessCheck(
            "node2_boundary_preserved",
            "Stage150 must inherit Node2 raw reveal zero from the sealed Page01 chain.",
            gate_rule_names.get("node2_boundary_preserved") is True,
            "stage148-stage149",
        ),
    )
    issues = [check.name for check in checks if not check.ready]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage149 Stage150 Readiness Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage150_memory_body_ready": not issues,
        "checks": [check.to_dict() for check in checks],
    }


def _build_release_blocker_registry(
    stage145: dict[str, Any],
    stage146: dict[str, Any],
    stage147: dict[str, Any],
    stage148: dict[str, Any],
) -> dict[str, Any]:
    latest = (
        _stage_payload(stage145, "stage145"),
        _stage_payload(stage146, "stage146"),
        _stage_payload(stage147, "stage147"),
        stage148,
    )
    blockers = (
        ReleaseBlocker("provider_calls", "Provider calls must remain blocked in Page01.", all(report.get("provider_default_calls") == 0 for report in latest), "release/current/stage148_node_boundary_constitution_report.json"),
        ReleaseBlocker("runtime_training", "Runtime training must remain blocked in Page01.", all(report.get("runtime_training_enabled") is False for report in latest), "release/current/stage145_body_constitution_report.json"),
        ReleaseBlocker("model_weight_update", "Model weight updates must remain blocked in Page01.", all(report.get("model_weight_update_count") == 0 for report in latest), "release/current/stage145_body_constitution_report.json"),
        ReleaseBlocker("losdb_write", "LOSDB writes must remain blocked in Page01.", all(report.get("losdb_write_enabled") is False for report in latest), "release/current/stage148_node_boundary_constitution_report.json"),
        ReleaseBlocker("migration_execution", "Migration execution must remain blocked in Page01.", all(report.get("migration_execution_enabled") is False for report in latest), "release/current/stage146_narrative_state_contract_report.json"),
        ReleaseBlocker("node2_raw_reveal_access", "Node2 raw reveal access must remain blocked in Page01.", all(report.get("node2_raw_reveal_access") == 0 for report in latest), "release/current/stage148_node_boundary_constitution_report.json"),
        ReleaseBlocker("canon_auto_resolution", "Automatic canon mutation must remain blocked in Page01.", all(report.get("canon_auto_resolution_count") == 0 for report in latest), "release/current/stage145_body_constitution_report.json"),
        ReleaseBlocker("auto_repair_mutation", "Automatic repair mutation must remain blocked in Page01.", all(report.get("auto_repair_mutation_count") == 0 for report in latest), "release/current/stage145_body_constitution_report.json"),
    )
    issues = [blocker.name for blocker in blockers if not blocker.blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage149 Release Blocker Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "registered_blocker_count": len(blockers),
        "blocked_capability_count": sum(1 for blocker in blockers if blocker.blocked),
        "all_blocked": not issues,
        "entries": [blocker.to_dict() for blocker in blockers],
    }


def _build_lineage_evidence_index(root: Path) -> dict[str, Any]:
    entries = (
        LineageEvidence("stage145", "Body Constitution", "release/current/stage145_body_constitution_report.json", "manifests/stage145_manifest.json", "docs/stages/stage145.md", _all_exist(root, "release/current/stage145_body_constitution_report.json", "manifests/stage145_manifest.json", "docs/stages/stage145.md")),
        LineageEvidence("stage146", "Narrative State Contract", "release/current/stage146_narrative_state_contract_report.json", "manifests/stage146_manifest.json", "docs/stages/stage146.md", _all_exist(root, "release/current/stage146_narrative_state_contract_report.json", "manifests/stage146_manifest.json", "docs/stages/stage146.md")),
        LineageEvidence("stage147", "Project Manifest Body", "release/current/stage147_project_manifest_body_report.json", "manifests/stage147_manifest.json", "docs/stages/stage147.md", _all_exist(root, "release/current/stage147_project_manifest_body_report.json", "manifests/stage147_manifest.json", "docs/stages/stage147.md")),
        LineageEvidence("stage148", "Node Boundary Constitution", "release/current/stage148_node_boundary_constitution_report.json", "manifests/stage148_manifest.json", "docs/stages/stage148.md", _all_exist(root, "release/current/stage148_node_boundary_constitution_report.json", "manifests/stage148_manifest.json", "docs/stages/stage148.md")),
    )
    issues = [entry.stage for entry in entries if not entry.present]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage149 Lineage Evidence Index",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "coverage_complete": not issues,
        "entries": [entry.to_dict() for entry in entries],
    }


def _all_exist(root: Path, *rels: str) -> bool:
    return all((root / rel).exists() for rel in rels)


def _stage_payload(report: dict[str, Any], key: str) -> dict[str, Any]:
    nested = report.get(key)
    if isinstance(nested, dict):
        return nested
    return report


def _compact_baseline(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "stage",
        "baseline_stage",
        "status",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["stage148_release_gate_status"] = report.get("status")
    return compact


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
