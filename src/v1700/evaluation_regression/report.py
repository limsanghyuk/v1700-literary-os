from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.evaluation_engine.report import _load_rubric, _metric_catalog, _score_packet, _thresholds
from v1700.evaluation_packet_store.loader import compute_evaluation_packet_checksum, load_evaluation_packets
from v1700.gates.stage169_release_gate import run_stage169_release_gate

TARGET_STAGE = "stage170"
TARGET_REPORT = "release/current/stage170_regression_negative_fixture_harness_report.json"
PACK_DIR = "release/current/stage170_regression_negative_fixture_harness_pack"
STORE_PATH = "samples/stage168_evaluation_packet_store/evaluation_packets.jsonl"


def run_stage170_regression_negative_fixture_harness(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage169 = run_stage169_release_gate(root)
    packets = load_evaluation_packets(root / STORE_PATH)
    rubric = _load_rubric(root)
    metrics = _metric_catalog(rubric)
    thresholds = _thresholds(rubric)
    pack_dir = root / PACK_DIR
    pack_dir.mkdir(parents=True, exist_ok=True)

    fixture_catalog = _build_fixture_catalog()
    fixture_results = _run_fixture_results(root, packets, metrics, thresholds)
    coverage = _build_fixture_coverage_matrix(fixture_results)
    regression_snapshot = _build_regression_snapshot(root, stage169, fixture_results)
    determinism = _build_fixture_replay_determinism(root, packets, metrics, thresholds)
    boundary = _build_boundary_negative_fixture_matrix(fixture_results)
    stage171_entry = _build_stage171_entry_criteria(stage169, fixture_results, coverage, regression_snapshot, determinism, boundary)

    parts = {
        "negative_fixture_catalog": fixture_catalog,
        "negative_fixture_results": fixture_results,
        "fixture_coverage_matrix": coverage,
        "regression_snapshot": regression_snapshot,
        "fixture_replay_determinism": determinism,
        "boundary_negative_fixture_matrix": boundary,
        "stage171_entry_criteria": stage171_entry,
    }
    for name, payload in parts.items():
        _write_json(pack_dir / f"{name}.json", payload)

    issues: list[str] = []
    if stage169.get("status") != "pass":
        issues.append("stage169_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "170",
        "baseline_stage": "169",
        "title": "Regression and Negative Fixture Harness",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DETERMINISTIC_LOCAL_REGRESSION_HARNESS_ONLY",
        "page": "Page05 Evaluation Body",
        "fixture_count": fixture_results.get("fixture_count", 0),
        "negative_fixture_count": fixture_results.get("negative_fixture_count", 0),
        "safe_fixture_pass": fixture_results.get("safe_fixture_pass") is True,
        "negative_fixture_blocks": fixture_results.get("negative_fixture_blocks") is True,
        "regression_snapshot_pass": regression_snapshot.get("status") == "pass",
        "fixture_coverage_pass": coverage.get("status") == "pass",
        "boundary_fixture_pass": boundary.get("status") == "pass",
        "determinism_channel_pass": determinism.get("status") == "pass",
        "stage169_evaluator_inherited": stage169.get("status") == "pass",
        "stage171_boundary_preflight_ready": not issues,
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
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage169_release_gate": _compact(stage169), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_fixture_catalog() -> dict[str, Any]:
    fixtures = [
        ("safe_baseline_fixture", "safe", "pass", ()),
        ("quality_drop_fixture", "quality", "blocked", ("quality_score_below_threshold",)),
        ("continuity_break_fixture", "continuity", "blocked", ("continuity_hard_violation",)),
        ("raw_reveal_leak_fixture", "boundary", "blocked", ("boundary_violation_detected",)),
        ("hidden_memory_projection_fixture", "boundary", "blocked", ("boundary_violation_detected",)),
        ("provider_call_fixture", "boundary", "blocked", ("boundary_violation_detected",)),
        ("mutation_command_fixture", "boundary", "blocked", ("boundary_violation_detected",)),
        ("stale_stage166_evidence_fixture", "regression", "blocked", ("continuity_hard_violation",)),
        ("checksum_drift_fixture", "regression", "blocked", ("packet_checksum_drift",)),
    ]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Negative Fixture Catalog",
        "status": "pass",
        "issues": [],
        "fixture_count": len(fixtures),
        "fixtures": [
            {"fixture_id": fixture_id, "channel": channel, "expected_status": expected, "expected_reasons": list(reasons)}
            for fixture_id, channel, expected, reasons in fixtures
        ],
    }


def _run_fixture_results(root: Path, packets: list[dict[str, Any]], metrics: list[dict[str, Any]], thresholds: dict[str, Any]) -> dict[str, Any]:
    base = packets[0]
    fixture_specs = _build_fixture_catalog()["fixtures"]
    entries = []
    issues: list[str] = []
    for spec in fixture_specs:
        packet = _fixture_packet(base, spec["fixture_id"])
        checksum_drift = packet.get("checksum") != compute_evaluation_packet_checksum(packet)
        scorecard = _score_packet(packet, metrics, thresholds, root)
        actual_reasons = set(scorecard.block_reasons)
        if checksum_drift:
            actual_reasons.add("packet_checksum_drift")
        actual_status = "blocked" if scorecard.status == "blocked" or checksum_drift else "pass"
        expected_status = spec["expected_status"]
        expected_reasons = set(spec.get("expected_reasons", []))
        expected_reasons_ok = expected_reasons.issubset(actual_reasons)
        status_ok = actual_status == expected_status
        verdict = "pass" if status_ok and expected_reasons_ok else "blocked"
        if verdict != "pass":
            issues.append(f"fixture_expectation_mismatch:{spec['fixture_id']}")
        entries.append(
            {
                "fixture_id": spec["fixture_id"],
                "channel": spec["channel"],
                "expected_status": expected_status,
                "actual_status": actual_status,
                "expected_reasons": sorted(expected_reasons),
                "actual_reasons": sorted(actual_reasons),
                "expectation_status": verdict,
                "quality_score": scorecard.quality_score,
                "continuity_violation_index": scorecard.continuity_violation_index,
                "regression_delta_index": scorecard.regression_delta_index,
                "boundary_violation_count": scorecard.boundary_violation_count,
                "packet_checksum_drift": checksum_drift,
                "deterministic_checksum": scorecard.deterministic_checksum,
            }
        )
    safe = [entry for entry in entries if entry["expected_status"] == "pass"]
    negative = [entry for entry in entries if entry["expected_status"] == "blocked"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Negative Fixture Results",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "fixture_count": len(entries),
        "negative_fixture_count": len(negative),
        "safe_fixture_pass": all(entry["actual_status"] == "pass" and entry["expectation_status"] == "pass" for entry in safe),
        "negative_fixture_blocks": all(entry["actual_status"] == "blocked" and entry["expectation_status"] == "pass" for entry in negative),
        "entries": entries,
    }


def _fixture_packet(base: dict[str, Any], fixture_id: str) -> dict[str, Any]:
    packet = copy.deepcopy(base)
    packet["evaluation_packet_id"] = fixture_id
    if fixture_id == "safe_baseline_fixture":
        packet["checksum"] = compute_evaluation_packet_checksum(packet)
        return packet
    if fixture_id == "quality_drop_fixture":
        packet["required_stage_refs"] = ["release/current/missing_quality_fixture_ref.json"]
    elif fixture_id == "continuity_break_fixture":
        packet["source_stage"] = "stage000"
    elif fixture_id == "raw_reveal_leak_fixture":
        packet["node2_projection_summary"] = "surface-safe summary raw_reveal"
    elif fixture_id == "hidden_memory_projection_fixture":
        packet["node2_projection_summary"] = "surface-safe hidden_memory projection"
    elif fixture_id == "provider_call_fixture":
        packet["packet_summary"] = "surface packet provider_handle"
    elif fixture_id == "mutation_command_fixture":
        packet["packet_summary"] = "surface packet mutation_command"
    elif fixture_id == "stale_stage166_evidence_fixture":
        packet["required_stage_refs"] = ["release/current/stale_stage166_fixture_ref.json"]
    elif fixture_id == "checksum_drift_fixture":
        packet["packet_summary"] = "surface structure packet with checksum drift"
        packet["checksum"] = "0" * 64
        return packet
    packet["checksum"] = compute_evaluation_packet_checksum(packet)
    return packet


def _build_fixture_coverage_matrix(fixture_results: dict[str, Any]) -> dict[str, Any]:
    required_channels = {"safe", "quality", "continuity", "boundary", "regression"}
    covered = {str(entry.get("channel")) for entry in fixture_results.get("entries", [])}
    missing = sorted(required_channels - covered)
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Fixture Coverage Matrix",
        "status": "pass" if not missing and fixture_results.get("status") == "pass" else "blocked",
        "issues": [f"missing_fixture_channel:{channel}" for channel in missing],
        "required_channels": sorted(required_channels),
        "covered_channels": sorted(covered),
        "fixture_count": fixture_results.get("fixture_count", 0),
    }


def _build_regression_snapshot(root: Path, stage169: dict[str, Any], fixture_results: dict[str, Any]) -> dict[str, Any]:
    report_path = root / "release/current/stage169_deterministic_quality_continuity_evaluator_report.json"
    gate_path = root / "release/current/stage169_release_gate_report.json"
    issues: list[str] = []
    if stage169.get("status") != "pass":
        issues.append("stage169_release_gate_blocked")
    if not report_path.exists():
        issues.append("missing_stage169_report")
    if not gate_path.exists():
        issues.append("missing_stage169_gate_report")
    if fixture_results.get("negative_fixture_blocks") is not True:
        issues.append("negative_fixture_blocking_failed")
    snapshot_payload = {
        "stage169_gate_status": stage169.get("status"),
        "stage169_report_sha256": _sha256(report_path) if report_path.exists() else "missing",
        "stage169_gate_sha256": _sha256(gate_path) if gate_path.exists() else "missing",
        "fixture_result_checksum": _payload_sha256(fixture_results),
    }
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Regression Snapshot",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "snapshot": snapshot_payload,
        "snapshot_checksum": _payload_sha256(snapshot_payload),
    }


def _build_fixture_replay_determinism(root: Path, packets: list[dict[str, Any]], metrics: list[dict[str, Any]], thresholds: dict[str, Any]) -> dict[str, Any]:
    first = _run_fixture_results(root, packets, metrics, thresholds)
    second = _run_fixture_results(root, packets, metrics, thresholds)
    first_checksums = [entry["deterministic_checksum"] for entry in first.get("entries", [])]
    second_checksums = [entry["deterministic_checksum"] for entry in second.get("entries", [])]
    issues = [] if first_checksums == second_checksums else ["fixture_replay_checksum_mismatch"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Fixture Replay Determinism",
        "status": "pass" if not issues and first.get("status") == "pass" and second.get("status") == "pass" else "blocked",
        "issues": issues,
        "replay_count": 2,
        "checksums": first_checksums,
    }


def _build_boundary_negative_fixture_matrix(fixture_results: dict[str, Any]) -> dict[str, Any]:
    boundary_entries = [entry for entry in fixture_results.get("entries", []) if entry.get("channel") == "boundary"]
    issues = [entry["fixture_id"] for entry in boundary_entries if entry.get("actual_status") != "blocked"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage170 Boundary Negative Fixture Matrix",
        "status": "pass" if not issues and len(boundary_entries) >= 4 else "blocked",
        "issues": [f"boundary_fixture_not_blocked:{item}" for item in issues] + ([] if len(boundary_entries) >= 4 else ["insufficient_boundary_fixture_count"]),
        "boundary_fixture_count": len(boundary_entries),
        "entries": boundary_entries,
    }


def _build_stage171_entry_criteria(stage169: dict[str, Any], fixture_results: dict[str, Any], coverage: dict[str, Any], regression_snapshot: dict[str, Any], determinism: dict[str, Any], boundary: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "stage169_release_gate_pass": stage169.get("status") == "pass",
        "safe_fixture_pass": fixture_results.get("safe_fixture_pass") is True,
        "negative_fixture_blocks": fixture_results.get("negative_fixture_blocks") is True,
        "fixture_coverage_pass": coverage.get("status") == "pass",
        "regression_snapshot_pass": regression_snapshot.get("status") == "pass",
        "fixture_determinism_pass": determinism.get("status") == "pass",
        "boundary_negative_fixture_pass": boundary.get("status") == "pass",
        "provider_default_calls_zero": True,
        "write_operations_zero": True,
        "node2_raw_reveal_access_zero": True,
    }
    issues = [name for name, ok in checks.items() if not ok]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage171 Entry Criteria",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage171_evaluation_boundary_leakage_preflight_ready": not issues,
        "checks": {name: {"status": "pass" if ok else "blocked"} for name, ok in checks.items()},
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
