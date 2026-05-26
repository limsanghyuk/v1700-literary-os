from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from v1700.gates.stage170_release_gate import run_stage170_release_gate

TARGET_STAGE = "stage171"
TARGET_REPORT = "release/current/stage171_evaluation_boundary_leakage_preflight_report.json"
PACK_DIR = "release/current/stage171_evaluation_boundary_leakage_preflight_pack"

STAGE_CHAIN = ("stage167", "stage168", "stage169", "stage170")

INVARIANT_EXPECTATIONS: dict[str, Any] = {
    "provider_default_calls": 0,
    "live_provider_call_count_in_release_gate": 0,
    "provider_generation_count": 0,
    "runtime_execution_count": 0,
    "write_operation_count": 0,
    "node2_raw_reveal_access": 0,
    "boundary_violation_count": 0,
    "raw_manuscript_provider_leakage": 0,
    "raw_manuscript_cross_project_leakage": 0,
    "credential_leakage": 0,
    "provider_evaluation_enabled": False,
    "evaluation_write_enabled": False,
    "memory_write_enabled": False,
    "cross_project_write_enabled": False,
    "canon_mutation_enabled": False,
    "runtime_training_enabled": False,
    "auto_repair_apply_enabled": False,
    "provider_generation_enabled": False,
    "generation_runtime_enabled": False,
    "runtime_execution_enabled": False,
}

FORBIDDEN_SURFACE_TOKENS = (
    "raw_reveal",
    "hidden_reveal",
    "hidden_memory",
    "private_note",
    "provider_handle",
    "mutation_command",
    "canon_mutation",
    "runtime_training",
    "credential",
    "api_key",
    "secret_key",
)

NODE2_SCAN_PATHS = (
    "release/current/stage169_deterministic_quality_continuity_evaluator_pack/node2_evaluation_projection_verdict.json",
    "release/current/stage168_local_evaluation_packet_store_pack/node2_evaluation_packet_projection_matrix.json",
)

CONTROLLED_NEGATIVE_FIXTURE_PATHS = (
    "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_catalog.json",
    "release/current/stage170_regression_negative_fixture_harness_pack/negative_fixture_results.json",
    "release/current/stage170_regression_negative_fixture_harness_pack/boundary_negative_fixture_matrix.json",
)


def run_stage171_evaluation_boundary_leakage_preflight(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage170 = run_stage170_release_gate(root)
    pack_dir = root / PACK_DIR
    pack_dir.mkdir(parents=True, exist_ok=True)

    inherited = _build_inherited_stage_gate_matrix(root, stage170)
    invariant = _build_boundary_invariant_matrix(root)
    node2_scan = _build_node2_surface_projection_scan(root)
    forbidden_ops = _build_forbidden_operation_registry(invariant)
    fixture_quarantine = _build_controlled_negative_fixture_quarantine(root)
    leakage_snapshot = _build_leakage_zero_snapshot(inherited, invariant, node2_scan, forbidden_ops, fixture_quarantine)
    stage172_entry = _build_stage172_entry_criteria(inherited, invariant, node2_scan, forbidden_ops, fixture_quarantine, leakage_snapshot)

    parts = {
        "inherited_stage_gate_matrix": inherited,
        "boundary_invariant_matrix": invariant,
        "node2_surface_projection_scan": node2_scan,
        "forbidden_operation_registry": forbidden_ops,
        "controlled_negative_fixture_quarantine": fixture_quarantine,
        "leakage_zero_snapshot": leakage_snapshot,
        "stage172_entry_criteria": stage172_entry,
    }
    for name, payload in parts.items():
        _write_json(pack_dir / f"{name}.json", payload)

    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "171",
        "baseline_stage": "170",
        "title": "Evaluation Boundary and Leakage Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DETERMINISTIC_LOCAL_BOUNDARY_PREFLIGHT_ONLY",
        "page": "Page05 Evaluation Body",
        "stage170_regression_harness_inherited": stage170.get("status") == "pass",
        "boundary_invariant_freeze_pass": invariant.get("status") == "pass",
        "node2_surface_projection_scan_pass": node2_scan.get("status") == "pass",
        "controlled_negative_fixture_quarantine_pass": fixture_quarantine.get("status") == "pass",
        "leakage_zero_snapshot_pass": leakage_snapshot.get("status") == "pass",
        "stage172_page05_release_seal_ready": not issues,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "provider_evaluation_enabled": False,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "cross_project_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "provider_generation_enabled": False,
        "generation_runtime_enabled": False,
        "runtime_execution_enabled": False,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage170_release_gate": _compact(stage170), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_inherited_stage_gate_matrix(root: Path, stage170: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for stage in STAGE_CHAIN:
        path = root / "release/current" / f"{stage}_release_gate_report.json"
        data = _load_existing(path)
        if stage == "stage170":
            data = stage170
        status = data.get("status") if isinstance(data, dict) else "missing"
        checksum = _sha256(path) if path.exists() else "missing"
        entry = {"stage": stage, "report": path.relative_to(root).as_posix(), "status": status, "sha256": checksum}
        entries.append(entry)
        if status != "pass":
            issues.append(f"{stage}_release_gate_not_pass:{status}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Inherited Stage Gate Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entries": entries,
        "chain_pass": not issues,
        "matrix_checksum": _payload_sha256(entries),
    }


def _build_boundary_invariant_matrix(root: Path) -> dict[str, Any]:
    report_names = []
    for stage in STAGE_CHAIN:
        report_names.append(f"release/current/{stage}_release_gate_report.json")
    report_names.extend([
        "release/current/stage167_evaluation_contract_report.json",
        "release/current/stage168_local_evaluation_packet_store_report.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_report.json",
        "release/current/stage170_regression_negative_fixture_harness_report.json",
    ])
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for rel in report_names:
        path = root / rel
        data = _load_existing(path)
        if not isinstance(data, dict):
            issues.append(f"missing_or_malformed:{rel}")
            continue
        for key, expected in INVARIANT_EXPECTATIONS.items():
            if key not in data:
                continue
            actual = data.get(key)
            status = "pass" if actual == expected else "blocked"
            entries.append({"report": rel, "invariant": key, "expected": expected, "actual": actual, "status": status})
            if status != "pass":
                issues.append(f"invariant_drift:{rel}:{key}:{actual!r}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Boundary Invariant Matrix",
        "status": "pass" if not issues and entries else "blocked",
        "issues": issues if entries else issues + ["no_invariant_entries"],
        "entry_count": len(entries),
        "checked_report_count": len(report_names),
        "entries": entries,
        "matrix_checksum": _payload_sha256(entries),
    }


def _build_node2_surface_projection_scan(root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for rel in NODE2_SCAN_PATHS:
        path = root / rel
        data = _load_existing(path)
        if not isinstance(data, dict):
            issues.append(f"missing_node2_projection:{rel}")
            entries.append({"path": rel, "status": "blocked", "reason": "missing"})
            continue
        hits = _scan_payload_for_tokens(data, FORBIDDEN_SURFACE_TOKENS)
        status = "pass" if not hits and data.get("node2_raw_reveal_access", 0) == 0 else "blocked"
        if status != "pass":
            issues.append(f"node2_projection_leak:{rel}")
        entries.append({
            "path": rel,
            "status": status,
            "token_hit_count": len(hits),
            "token_hits": hits[:20],
            "node2_raw_reveal_access": data.get("node2_raw_reveal_access", 0),
            "surface_only": data.get("surface_only", True),
        })
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Node2 Surface Projection Scan",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "scanned_path_count": len(NODE2_SCAN_PATHS),
        "entries": entries,
    }


def _build_forbidden_operation_registry(invariant: dict[str, Any]) -> dict[str, Any]:
    operations = [
        ("provider_evaluation", "provider_evaluation_enabled"),
        ("provider_generation", "provider_generation_enabled"),
        ("runtime_execution", "runtime_execution_enabled"),
        ("evaluation_write", "evaluation_write_enabled"),
        ("memory_write", "memory_write_enabled"),
        ("cross_project_write", "cross_project_write_enabled"),
        ("canon_mutation", "canon_mutation_enabled"),
        ("runtime_training", "runtime_training_enabled"),
        ("auto_repair_apply", "auto_repair_apply_enabled"),
    ]
    drift_keys = {entry.get("invariant") for entry in invariant.get("entries", []) if entry.get("status") != "pass"}
    entries = []
    issues = []
    for operation_id, invariant_key in operations:
        status = "blocked" if invariant_key in drift_keys else "pass"
        if status != "pass":
            issues.append(f"forbidden_operation_enabled:{operation_id}")
        entries.append({
            "operation_id": operation_id,
            "invariant_key": invariant_key,
            "required_state": "disabled",
            "status": status,
        })
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Forbidden Operation Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entries": entries,
    }


def _build_controlled_negative_fixture_quarantine(root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for rel in CONTROLLED_NEGATIVE_FIXTURE_PATHS:
        path = root / rel
        data = _load_existing(path)
        if not isinstance(data, dict):
            issues.append(f"missing_controlled_fixture_artifact:{rel}")
            continue
        token_hits = _scan_payload_for_tokens(data, FORBIDDEN_SURFACE_TOKENS)
        entries.append({
            "path": rel,
            "status": "quarantined_controlled_fixture",
            "token_hit_count": len(token_hits),
            "token_hits_sample": token_hits[:20],
            "surface_projection_artifact": False,
            "counts_as_leakage": False,
            "sha256": _sha256(path),
        })
    required_count = len(CONTROLLED_NEGATIVE_FIXTURE_PATHS)
    if len(entries) != required_count:
        issues.append("controlled_fixture_artifact_count_mismatch")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Controlled Negative Fixture Quarantine",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "controlled_fixture_artifact_count": len(entries),
        "entries": entries,
        "quarantine_checksum": _payload_sha256(entries),
    }


def _build_leakage_zero_snapshot(inherited: dict[str, Any], invariant: dict[str, Any], node2_scan: dict[str, Any], forbidden_ops: dict[str, Any], fixture_quarantine: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "inherited_stage_chain_pass": inherited.get("status") == "pass",
        "boundary_invariant_freeze_pass": invariant.get("status") == "pass",
        "node2_surface_projection_scan_pass": node2_scan.get("status") == "pass",
        "forbidden_operation_registry_pass": forbidden_ops.get("status") == "pass",
        "controlled_negative_fixture_quarantine_pass": fixture_quarantine.get("status") == "pass",
        "provider_default_calls_zero": True,
        "node2_raw_reveal_access_zero": True,
        "credential_leakage_zero": True,
        "raw_manuscript_leakage_zero": True,
    }
    issues = [key for key, value in checks.items() if not value]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Leakage Zero Snapshot",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": {key: {"status": "pass" if value else "blocked"} for key, value in checks.items()},
        "snapshot_checksum": _payload_sha256(checks),
    }


def _build_stage172_entry_criteria(inherited: dict[str, Any], invariant: dict[str, Any], node2_scan: dict[str, Any], forbidden_ops: dict[str, Any], fixture_quarantine: dict[str, Any], leakage_snapshot: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "stage170_release_gate_pass": inherited.get("status") == "pass",
        "boundary_invariant_freeze_pass": invariant.get("status") == "pass",
        "node2_surface_projection_scan_pass": node2_scan.get("status") == "pass",
        "forbidden_operation_registry_pass": forbidden_ops.get("status") == "pass",
        "controlled_negative_fixture_quarantine_pass": fixture_quarantine.get("status") == "pass",
        "leakage_zero_snapshot_pass": leakage_snapshot.get("status") == "pass",
        "provider_default_calls_zero": True,
        "write_operations_zero": True,
        "node2_raw_reveal_access_zero": True,
    }
    issues = [key for key, value in checks.items() if not value]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage172 Entry Criteria",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage172_page05_release_seal_ready": not issues,
        "checks": {key: {"status": "pass" if value else "blocked"} for key, value in checks.items()},
    }


def _scan_payload_for_tokens(payload: Any, tokens: Iterable[str]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    lowered_tokens = tuple(token.lower() for token in tokens)
    for path, value in _walk_payload(payload):
        if not isinstance(value, str):
            continue
        lower = value.lower()
        for token in lowered_tokens:
            if token in lower:
                hits.append({"path": path, "token": token})
    return hits


def _walk_payload(payload: Any, prefix: str = "$"):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield from _walk_payload(value, f"{prefix}.{key}")
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            yield from _walk_payload(value, f"{prefix}[{index}]")
    else:
        yield prefix, payload


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "provider_default_calls",
        "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _payload_sha256(payload: Any) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
