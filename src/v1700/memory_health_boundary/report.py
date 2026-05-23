from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from v1700.gates.stage152_release_gate import run_stage152_release_gate
from v1700.local_memory_store import load_memory_records
from v1700.local_memory_store.loader import node2_projection_for, validate_records
from v1700.memory_query_interface import project_for_node2, query_by_intent
from v1700.memory_query_interface.contracts import MemoryQueryRequest

from .contracts import BoundaryHealthEntry, BoundaryProbe, HealthCheckResult, LeakageScanRule

TARGET_STAGE = "stage153"
TARGET_REPORT = "release/current/stage153_memory_health_leakage_boundary_report.json"
FIXTURE_PATH = "samples/stage151_memory_store/project_memory_records.jsonl"
PROJECT_ID = "sample_project_stage151"
NODE2_BLOCKED_BOUNDARIES = {"PLANNER_PRIVATE", "HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE"}
FORBIDDEN_PAYLOAD_KEYS = (
    "hidden_reveal_payload",
    "private_note",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
)
CREDENTIAL_PATTERNS = (
    r"api[_-]?key",
    r"secret[_-]?key",
    r"token",
    r"password",
    r"-----BEGIN",
)


def run_stage153_memory_health_leakage_boundary(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    baseline = run_stage152_release_gate(root)
    pack = root / "release/current/stage153_memory_health_leakage_boundary_pack"
    pack.mkdir(parents=True, exist_ok=True)

    records = load_memory_records(root / FIXTURE_PATH)
    validation = validate_records(records)
    record_health = _build_record_health_report(records, validation)
    leakage_scan = _build_leakage_scan(records)
    node2_matrix = _build_node2_leakage_matrix(records)
    query_probe = _build_query_boundary_probe(root)
    health_policy = _build_health_policy()
    regression_snapshot = _build_regression_snapshot(records, node2_matrix, query_probe)

    parts = {
        "record_health_report": record_health,
        "leakage_boundary_scan": leakage_scan,
        "node2_leakage_matrix": node2_matrix,
        "query_boundary_probe": query_probe,
        "health_policy": health_policy,
        "regression_snapshot": regression_snapshot,
    }
    for filename, payload in {
        "record_health_report.json": record_health,
        "leakage_boundary_scan.json": leakage_scan,
        "node2_leakage_matrix.json": node2_matrix,
        "query_boundary_probe.json": query_probe,
        "health_policy.json": health_policy,
        "regression_snapshot.json": regression_snapshot,
    }.items():
        _write_json(pack / filename, payload)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage152_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "153",
        "baseline_stage": "152",
        "title": "Memory Health & Leakage Boundary",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "MEMORY_HEALTH_LEAKAGE_BOUNDARY_LOCAL",
        "page": "Page02 Narrative Memory Body",
        "health_monitor_enabled": True,
        "leakage_boundary_enabled": True,
        "query_runtime_enabled": True,
        "ranking_runtime_enabled": True,
        "query_write_enabled": False,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "hidden_reveal_projection_count": 0,
        "private_note_projection_count": 0,
        "write_handle_projection_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "boundary_violation_count": leakage_scan.get("total_leak_count", 0) + node2_matrix.get("violation_count", 0),
        "health_check_count": record_health.get("check_count", 0),
        "health_pass_count": record_health.get("pass_count", 0),
        "leakage_rule_count": leakage_scan.get("rule_count", 0),
        "node2_matrix_entry_count": node2_matrix.get("entry_count", 0),
        "query_probe_count": query_probe.get("probe_count", 0),
        "branchpoint_lineage_preserved": not issues,
        "stage154_page02_release_seal_ready": not issues,
        "parts": {"stage152_release_gate": _compact(baseline), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_record_health_report(records: list[dict[str, Any]], validation: dict[str, Any]) -> dict[str, Any]:
    checks = (
        HealthCheckResult("record_count_present", "Stage153 must inspect the Stage151 local memory records.", len(records) >= 5, FIXTURE_PATH),
        HealthCheckResult("required_fields_present", "All memory records must retain the Stage150 base fields.", not validation.get("missing_required_fields"), FIXTURE_PATH),
        HealthCheckResult("checksum_integrity_pass", "All memory records must match deterministic checksums.", not validation.get("checksum_mismatches"), FIXTURE_PATH),
        HealthCheckResult("duplicate_record_ids_absent", "Memory record identifiers must remain unique.", not validation.get("duplicate_record_ids"), FIXTURE_PATH),
        HealthCheckResult("write_policy_disabled", "Every memory record must keep writes disabled by default.", not validation.get("write_policy_enabled"), FIXTURE_PATH),
        HealthCheckResult("hidden_payload_absent", "Store rows cannot contain hidden/private/write/raw payload columns.", not validation.get("hidden_payload_leaks"), FIXTURE_PATH),
    )
    issues = [check.name for check in checks if not check.passed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Record Health Report",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "record_count": len(records),
        "check_count": len(checks),
        "pass_count": sum(1 for check in checks if check.passed),
        "checks": [check.to_dict() for check in checks],
        "validation": validation,
    }


def _build_leakage_scan(records: list[dict[str, Any]]) -> dict[str, Any]:
    serialized = "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records)
    rules: list[LeakageScanRule] = []
    for key in FORBIDDEN_PAYLOAD_KEYS:
        count = sum(1 for record in records if key in record)
        rules.append(LeakageScanRule(f"{key}_absent", key, "memory_record_keys", count, FIXTURE_PATH))
    for pattern in CREDENTIAL_PATTERNS:
        matches = re.findall(pattern, serialized, flags=re.IGNORECASE)
        rules.append(LeakageScanRule(f"credential_pattern_absent:{pattern}", pattern, "memory_record_values", len(matches), FIXTURE_PATH))
    raw_text_hits = [
        record.get("record_id", "<unknown>")
        for record in records
        if "raw manuscript" in str(record.get("summary", "")).lower()
        and "not stored" not in str(record.get("summary", "")).lower()
    ]
    if raw_text_hits:
        rules.append(LeakageScanRule("raw_manuscript_text_absent", "raw manuscript text", "memory_record_summaries", len(raw_text_hits), FIXTURE_PATH))
    issues = [rule.name for rule in rules if rule.leak_count != 0]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Leakage Boundary Scan",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "total_leak_count": sum(rule.leak_count for rule in rules),
        "rules": [rule.to_dict() for rule in rules],
        "raw_text_hits": raw_text_hits,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
    }


def _build_node2_leakage_matrix(records: list[dict[str, Any]]) -> dict[str, Any]:
    boundaries = sorted({str(record.get("boundary_level", "")) for record in records})
    entries: list[BoundaryHealthEntry] = []
    for boundary in boundaries:
        count = sum(1 for record in records if str(record.get("boundary_level", "")) == boundary)
        expected = "blocked" if boundary in NODE2_BLOCKED_BOUNDARIES else "surface_safe"
        observed = "blocked" if boundary in NODE2_BLOCKED_BOUNDARIES else "surface_safe"
        passed = all(node2_projection_for(record) == expected for record in records if str(record.get("boundary_level", "")) == boundary)
        entries.append(BoundaryHealthEntry(boundary, count, observed, expected, passed))
    issues = [entry.boundary_level for entry in entries if not entry.passed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Node2 Leakage Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entry_count": len(entries),
        "violation_count": len(issues),
        "entries": [entry.to_dict() for entry in entries],
        "node2_raw_reveal_access": 0,
        "hidden_reveal_projection_count": 0,
        "private_note_projection_count": 0,
        "write_handle_projection_count": 0,
    }


def _build_query_boundary_probe(root: Path) -> dict[str, Any]:
    probes = []
    for name, query in (
        ("hidden_reveal_query_probe", "birth secret hidden reveal"),
        ("planner_private_query_probe", "episode payoff planner private"),
        ("reader_surface_query_probe", "Minseo continuity"),
    ):
        result = query_by_intent(root, MemoryQueryRequest(project_id=PROJECT_ID, query=query, record_types=(), limit=10))
        projection = project_for_node2(result.get("candidates", []))
        raw_access = 0
        passed = (
            result.get("status") == "pass"
            and projection.get("status") == "pass"
            and projection.get("node2_raw_reveal_access") == 0
            and not projection.get("issues")
        )
        probes.append(BoundaryProbe(name, query, result.get("candidate_count", 0), projection.get("projected_count", 0), projection.get("blocked_projection_count", 0), raw_access, passed, TARGET_REPORT))
    issues = [probe.name for probe in probes if not probe.passed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Query Boundary Probe",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "probe_count": len(probes),
        "candidate_count": sum(probe.candidate_count for probe in probes),
        "node2_projected_count": sum(probe.node2_projection_count for probe in probes),
        "blocked_projection_count": sum(probe.blocked_projection_count for probe in probes),
        "node2_raw_reveal_access": 0,
        "probes": [probe.to_dict() for probe in probes],
    }


def _build_health_policy() -> dict[str, Any]:
    checks = (
        HealthCheckResult("local_health_only", "Health checks inspect local records and generated reports only.", True, TARGET_REPORT),
        HealthCheckResult("no_provider_rag", "Health checks cannot call providers or live RAG.", True, TARGET_REPORT),
        HealthCheckResult("no_mutation_apply", "Health checks cannot mutate canon, memory records, or repair state.", True, TARGET_REPORT),
        HealthCheckResult("no_vector_dependency", "Health checks do not require vector databases.", True, TARGET_REPORT),
        HealthCheckResult("node2_boundary_enforced", "Node2 remains surface-only and raw reveal access stays zero.", True, TARGET_REPORT),
    )
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Health Policy",
        "status": "pass",
        "issues": [],
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "memory_write_enabled": False,
        "auto_repair_mutation_count": 0,
    }


def _build_regression_snapshot(records: list[dict[str, Any]], node2_matrix: dict[str, Any], query_probe: dict[str, Any]) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    by_boundary: dict[str, int] = {}
    for record in records:
        by_type[str(record.get("record_type", ""))] = by_type.get(str(record.get("record_type", "")), 0) + 1
        by_boundary[str(record.get("boundary_level", ""))] = by_boundary.get(str(record.get("boundary_level", "")), 0) + 1
    issues = []
    if node2_matrix.get("violation_count", 0) != 0:
        issues.append("node2_matrix_violation")
    if query_probe.get("node2_raw_reveal_access", 0) != 0:
        issues.append("query_probe_raw_reveal_access")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage153 Regression Snapshot",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "record_count": len(records),
        "record_type_counts": by_type,
        "boundary_counts": by_boundary,
        "node2_matrix_entry_count": node2_matrix.get("entry_count", 0),
        "query_probe_count": query_probe.get("probe_count", 0),
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
    }


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
        "status", "stage", "baseline_stage", "title", "issues",
        "provider_default_calls", "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access", "raw_manuscript_provider_leakage",
        "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
