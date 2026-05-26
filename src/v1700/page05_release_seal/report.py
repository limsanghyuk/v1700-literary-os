from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.gates.stage167_release_gate import run_stage167_release_gate
from v1700.gates.stage168_release_gate import run_stage168_release_gate
from v1700.gates.stage169_release_gate import run_stage169_release_gate
from v1700.gates.stage170_release_gate import run_stage170_release_gate
from v1700.gates.stage171_release_gate import run_stage171_release_gate

TARGET_STAGE = "stage172"
TARGET_REPORT = "release/current/stage172_page05_release_seal_report.json"
PACK_DIR = "release/current/stage172_page05_release_seal_pack"

PAGE05_UPSTREAM_STAGES: tuple[tuple[str, str, str, str], ...] = (
    ("167", "Evaluation Contract", "release/current/stage167_evaluation_contract_report.json", "release/current/stage167_release_gate_report.json"),
    ("168", "Local Evaluation Packet Store", "release/current/stage168_local_evaluation_packet_store_report.json", "release/current/stage168_release_gate_report.json"),
    ("169", "Deterministic Quality and Continuity Evaluator", "release/current/stage169_deterministic_quality_continuity_evaluator_report.json", "release/current/stage169_release_gate_report.json"),
    ("170", "Regression and Negative Fixture Harness", "release/current/stage170_regression_negative_fixture_harness_report.json", "release/current/stage170_release_gate_report.json"),
    ("171", "Evaluation Boundary and Leakage Preflight", "release/current/stage171_evaluation_boundary_leakage_preflight_report.json", "release/current/stage171_release_gate_report.json"),
)
PAGE05_TOTAL_STAGE_COUNT = len(PAGE05_UPSTREAM_STAGES) + 1

CURRENT_STAGE_GENERATED_ASSETS = {
    TARGET_REPORT,
    "release/current/stage172_release_gate_report.json",
    "release/current/stage172_summary.json",
    f"{PACK_DIR}/page05_stage_chain.json",
    f"{PACK_DIR}/page05_release_seal_matrix.json",
    f"{PACK_DIR}/page05_artifact_index.json",
    f"{PACK_DIR}/page05_invariant_freeze.json",
    f"{PACK_DIR}/page05_evaluation_evidence_matrix.json",
    f"{PACK_DIR}/page05_transition_criteria.json",
    f"{PACK_DIR}/page05_release_seal.json",
    f"{PACK_DIR}/regression_snapshot.json",
}

CORE_PAGE05_INVARIANTS: dict[str, int | bool] = {
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


def run_stage172_page05_release_seal(root: Path | None = None, mode: str = "active") -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    active_version = _active_version(root)
    if active_version != TARGET_STAGE:
        existing = _load_json(root / TARGET_REPORT)
        if mode == "historical" and existing is not None:
            return existing
        return {
            "stage": "172",
            "baseline_stage": "171",
            "title": "Page05 Release Seal",
            "status": "blocked",
            "issues": [f"active_version_mismatch:{active_version or 'missing'}"],
            "mode": "PAGE05_RELEASE_SEAL_ACTIVE",
            "page": "Page05 Evaluation Body",
            "page05_release_seal_only": True,
            "page05_sealed": False,
            "page05_stage_count": PAGE05_TOTAL_STAGE_COUNT,
            "page05_total_stage_count": PAGE05_TOTAL_STAGE_COUNT,
            "stage173_governance_contract_ready": False,
            "next_stage": "stage173",
            "next_stage_title": "Governance Contract",
            "next_page": "Page06 Governance Body",
            "provider_default_calls": 0,
            "node2_raw_reveal_access": 0,
            "branchpoint_lineage_preserved": False,
        }

    gates = (
        _gate_or_existing(root, "stage167_release_gate_report.json", run_stage167_release_gate),
        _gate_or_existing(root, "stage168_release_gate_report.json", run_stage168_release_gate),
        _gate_or_existing(root, "stage169_release_gate_report.json", run_stage169_release_gate),
        _gate_or_existing(root, "stage170_release_gate_report.json", run_stage170_release_gate),
        _gate_or_existing(root, "stage171_release_gate_report.json", run_stage171_release_gate),
    )
    pack = root / PACK_DIR
    pack.mkdir(parents=True, exist_ok=True)

    stage_chain = _build_stage_chain(root, gates)
    release_matrix = _build_release_seal_matrix(stage_chain)
    invariant_freeze = _build_invariant_freeze(root, gates)
    evidence_matrix = _build_evaluation_evidence_matrix(root)
    regression = _build_regression_snapshot(root, stage_chain, invariant_freeze, evidence_matrix)
    transition = _build_transition_criteria(stage_chain, invariant_freeze, evidence_matrix, regression)

    pre_index_parts = {
        "page05_stage_chain": stage_chain,
        "page05_release_seal_matrix": release_matrix,
        "page05_invariant_freeze": invariant_freeze,
        "page05_evaluation_evidence_matrix": evidence_matrix,
        "page05_transition_criteria": transition,
        "regression_snapshot": regression,
    }
    for name, payload in pre_index_parts.items():
        _write_json(pack / f"{name}.json", payload)

    artifact_index = _build_artifact_index(root)
    seal = _build_page05_release_seal(pre_index_parts, artifact_index)
    _write_json(pack / "page05_artifact_index.json", artifact_index)
    _write_json(pack / "page05_release_seal.json", seal)

    parts = {**pre_index_parts, "page05_artifact_index": artifact_index, "page05_release_seal": seal}
    issues: list[str] = []
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "172",
        "baseline_stage": "171",
        "title": "Page05 Release Seal",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "PAGE05_RELEASE_SEAL_LOCAL",
        "page": "Page05 Evaluation Body",
        "page05_release_seal_only": True,
        "page05_sealed": not issues,
        "page05_stage_count": PAGE05_TOTAL_STAGE_COUNT,
        "page05_total_stage_count": PAGE05_TOTAL_STAGE_COUNT,
        "page05_upstream_stage_count": len(PAGE05_UPSTREAM_STAGES),
        "page05_stage_chain_pass": stage_chain.get("status") == "pass",
        "page05_artifact_index_complete": artifact_index.get("status") == "pass",
        "page05_invariant_freeze_pass": invariant_freeze.get("status") == "pass",
        "page05_evaluation_evidence_pass": evidence_matrix.get("status") == "pass",
        "page05_regression_snapshot_pass": regression.get("status") == "pass",
        "page05_release_checksum": seal.get("page05_release_checksum"),
        "stage173_governance_contract_ready": not issues,
        "next_stage": "stage173",
        "next_stage_title": "Governance Contract",
        "next_page": "Page06 Governance Body",
        "quality_channel_pass": evidence_matrix.get("quality_channel_pass") is True,
        "continuity_channel_pass": evidence_matrix.get("continuity_channel_pass") is True,
        "regression_channel_pass": evidence_matrix.get("regression_channel_pass") is True,
        "boundary_channel_pass": evidence_matrix.get("boundary_channel_pass") is True,
        "determinism_channel_pass": evidence_matrix.get("determinism_channel_pass") is True,
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
        "parts": parts,
    }
    _write_json(root / TARGET_REPORT, result)
    _write_json(root / "release/current/stage172_summary.json", _compact(result))
    return result


def _build_stage_chain(root: Path, gates: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    stages: list[dict[str, Any]] = []
    issues: list[str] = []
    for (stage, title, report_path, gate_path), gate in zip(PAGE05_UPSTREAM_STAGES, gates):
        report = _load_json(root / report_path) or {}
        gate_report = _load_json(root / gate_path) or gate
        sealed = report.get("status") == "pass" and gate_report.get("status") == "pass"
        status = "pass" if sealed else "blocked"
        if not sealed:
            issues.append(f"stage{stage}_not_sealed")
        stages.append({
            "stage": stage,
            "title": title,
            "report_path": report_path,
            "gate_path": gate_path,
            "report_status": report.get("status", "missing"),
            "gate_status": gate_report.get("status", "missing"),
            "status": status,
            "sealed": sealed,
            "report_sha256": _sha256(root / report_path) if (root / report_path).exists() else "missing",
            "gate_sha256": _sha256(root / gate_path) if (root / gate_path).exists() else "missing",
        })
    return {
        "stage": TARGET_STAGE,
        "title": "Page05 Upstream Stage Chain",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "stage_count": len(stages),
        "sealed_count": sum(1 for item in stages if item["sealed"]),
        "stages": stages,
        "matrix_checksum": _payload_sha256(stages),
    }


def _build_release_seal_matrix(stage_chain: dict[str, Any]) -> dict[str, Any]:
    checks = [
        ("upstream_stage_chain_complete", stage_chain.get("status") == "pass" and stage_chain.get("stage_count") == len(PAGE05_UPSTREAM_STAGES), "Stage167 through Stage171 all pass before Stage172 seals Page05."),
        ("evaluation_contract_sealed", _stage_sealed(stage_chain, "167"), "Evaluation contract is sealed."),
        ("evaluation_packet_store_sealed", _stage_sealed(stage_chain, "168"), "Local evaluation packet store is sealed."),
        ("quality_continuity_evaluator_sealed", _stage_sealed(stage_chain, "169"), "Deterministic evaluator is sealed."),
        ("regression_harness_sealed", _stage_sealed(stage_chain, "170"), "Regression and negative fixture harness is sealed."),
        ("boundary_preflight_sealed", _stage_sealed(stage_chain, "171"), "Boundary and leakage preflight is sealed."),
    ]
    rows = [{"check_id": name, "status": "pass" if ok else "blocked", "description": desc} for name, ok, desc in checks]
    issues = [row["check_id"] for row in rows if row["status"] != "pass"]
    return {"stage": TARGET_STAGE, "title": "Page05 Release Seal Matrix", "status": "pass" if not issues else "blocked", "issues": issues, "checks": rows}


def _build_invariant_freeze(root: Path, gates: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    sources = _upstream_evidence_sources(root, gates)
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for source_name, source_path, payload in sources:
        for invariant_name, expected in CORE_PAGE05_INVARIANTS.items():
            if invariant_name not in payload:
                entries.append({"source": source_name, "path": source_path, "name": invariant_name, "expected": expected, "observed": None, "status": "skipped", "reason": "not_declared_in_legacy_page05_evidence"})
                continue
            observed = payload.get(invariant_name)
            status = "pass" if observed == expected else "blocked"
            if status != "pass":
                issues.append(f"{source_name}_invariant_drift:{invariant_name}")
            entries.append({"source": source_name, "path": source_path, "name": invariant_name, "expected": expected, "observed": observed, "status": status, "reason": "match" if status == "pass" else "drift"})
    return {
        "stage": TARGET_STAGE,
        "title": "Page05 Invariant Freeze",
        "status": "pass" if not issues and entries else "blocked",
        "issues": issues if entries else ["no_invariant_entries"],
        "entry_count": len(entries),
        "source_count": len(sources),
        "invariant_count": len(CORE_PAGE05_INVARIANTS),
        "entries": entries,
        "matrix_checksum": _payload_sha256(entries),
    }


def _build_evaluation_evidence_matrix(root: Path) -> dict[str, Any]:
    stage169 = _load_json(root / "release/current/stage169_deterministic_quality_continuity_evaluator_report.json") or {}
    stage170 = _load_json(root / "release/current/stage170_regression_negative_fixture_harness_report.json") or {}
    stage171 = _load_json(root / "release/current/stage171_evaluation_boundary_leakage_preflight_report.json") or {}
    checks = [
        ("quality_channel_pass", stage169.get("quality_channel_pass") is True),
        ("continuity_channel_pass", stage169.get("continuity_channel_pass") is True),
        ("determinism_channel_pass", stage169.get("determinism_channel_pass") is True and stage170.get("determinism_channel_pass") is True),
        ("regression_channel_pass", stage170.get("regression_snapshot_pass") is True and stage170.get("negative_fixture_blocks") is True),
        ("boundary_channel_pass", stage171.get("boundary_invariant_freeze_pass") is True and stage171.get("leakage_zero_snapshot_pass") is True and stage171.get("node2_surface_projection_scan_pass") is True),
        ("stage172_entry_ready", stage171.get("stage172_page05_release_seal_ready") is True),
    ]
    entries = [{"channel": name, "status": "pass" if ok else "blocked"} for name, ok in checks]
    issues = [entry["channel"] for entry in entries if entry["status"] != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Page05 Evaluation Evidence Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "quality_channel_pass": entries[0]["status"] == "pass",
        "continuity_channel_pass": entries[1]["status"] == "pass",
        "determinism_channel_pass": entries[2]["status"] == "pass",
        "regression_channel_pass": entries[3]["status"] == "pass",
        "boundary_channel_pass": entries[4]["status"] == "pass",
        "stage172_entry_ready": entries[5]["status"] == "pass",
        "entries": entries,
        "source_reports": {
            "stage169": _compact(stage169),
            "stage170": _compact(stage170),
            "stage171": _compact(stage171),
        },
        "matrix_checksum": _payload_sha256(entries),
    }


def _build_regression_snapshot(root: Path, stage_chain: dict[str, Any], invariant_freeze: dict[str, Any], evidence_matrix: dict[str, Any]) -> dict[str, Any]:
    filelist = _read_lines(root / "FILELIST.txt") if (root / "FILELIST.txt").exists() else []
    forbidden = [entry for entry in filelist if _is_forbidden_entry(entry)]
    snapshot = {
        "stage_chain_checksum": stage_chain.get("matrix_checksum"),
        "invariant_freeze_checksum": invariant_freeze.get("matrix_checksum"),
        "evaluation_evidence_checksum": evidence_matrix.get("matrix_checksum"),
        "filelist_entry_count": len(filelist),
        "forbidden_cache_entries": len(forbidden),
        "forbidden_cache_entry_sample": forbidden[:20],
    }
    issues = []
    if forbidden:
        issues.append("forbidden_cache_entries_present")
    if not all(snapshot[k] for k in ("stage_chain_checksum", "invariant_freeze_checksum", "evaluation_evidence_checksum")):
        issues.append("missing_snapshot_checksum")
    return {"stage": TARGET_STAGE, "title": "Page05 Regression Snapshot", "status": "pass" if not issues else "blocked", "issues": issues, **snapshot, "snapshot_checksum": _payload_sha256(snapshot)}


def _build_transition_criteria(stage_chain: dict[str, Any], invariant_freeze: dict[str, Any], evidence_matrix: dict[str, Any], regression: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "page05_stage_chain_pass": stage_chain.get("status") == "pass",
        "page05_invariant_freeze_pass": invariant_freeze.get("status") == "pass",
        "quality_channel_pass": evidence_matrix.get("quality_channel_pass") is True,
        "continuity_channel_pass": evidence_matrix.get("continuity_channel_pass") is True,
        "regression_channel_pass": evidence_matrix.get("regression_channel_pass") is True,
        "boundary_channel_pass": evidence_matrix.get("boundary_channel_pass") is True,
        "determinism_channel_pass": evidence_matrix.get("determinism_channel_pass") is True,
        "regression_snapshot_pass": regression.get("status") == "pass",
    }
    entries = [{"criterion": k, "status": "pass" if v else "blocked"} for k, v in checks.items()]
    issues = [entry["criterion"] for entry in entries if entry["status"] != "pass"]
    return {"stage": TARGET_STAGE, "title": "Stage173 Governance Contract Entry Criteria", "status": "pass" if not issues else "blocked", "issues": issues, "stage173_governance_contract_ready": not issues, "criteria": entries}


def _build_artifact_index(root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    issues: list[str] = []
    for rel in sorted(_expected_artifacts()):
        path = root / rel
        exists = path.exists() or rel in CURRENT_STAGE_GENERATED_ASSETS
        entries.append({"path": rel, "exists": exists, "sha256": _sha256(path) if path.exists() else "generated_or_missing"})
        if not exists:
            issues.append(f"missing:{rel}")
    return {"stage": TARGET_STAGE, "title": "Page05 Artifact Index", "status": "pass" if not issues else "blocked", "issues": issues, "artifact_count": len(entries), "entries": entries, "index_checksum": _payload_sha256(entries)}


def _build_page05_release_seal(parts: dict[str, Any], artifact_index: dict[str, Any]) -> dict[str, Any]:
    payload = {"parts": {name: value.get("status") for name, value in parts.items()}, "artifact_index_status": artifact_index.get("status")}
    issues = [name for name, value in parts.items() if value.get("status") != "pass"]
    if artifact_index.get("status") != "pass":
        issues.append("artifact_index_blocked")
    checksum = _payload_sha256({"parts": parts, "artifact_index": artifact_index})
    return {"stage": TARGET_STAGE, "title": "Page05 Release Seal", "status": "pass" if not issues else "blocked", "issues": issues, "page05_sealed": not issues, "page05_release_checksum": checksum, "summary": payload}


def _expected_artifacts() -> set[str]:
    docs = {
        "docs/stages/stage172.md",
        "docs/proposals/stage172_page05_release_seal_proposal.md",
        "docs/architecture/stage172_page05_release_seal_blueprint.md",
        "docs/development/stage172_developer_handoff.md",
        "docs/proposals/page05_evaluation_body_proposal.md",
        "docs/architecture/page05_evaluation_body_blueprint.md",
        "docs/development/page05_developer_handoff.md",
    }
    manifests = {
        "manifests/stage172_manifest.json",
        "manifests/stage172_page05_release_seal_manifest.json",
        "manifests/stage172_branchpoint_trace_manifest.json",
        "manifests/live_core_stage172_overlay.json",
    }
    release = {
        "release/current/stage172_release_asset_manifest.json",
        "release/current/stage172_page05_release_seal_report.json",
        "release/current/stage172_release_gate_report.json",
        "release/current/stage172_summary.json",
    }
    pack = {f"{PACK_DIR}/{name}.json" for name in ("page05_stage_chain", "page05_release_seal_matrix", "page05_artifact_index", "page05_invariant_freeze", "page05_evaluation_evidence_matrix", "page05_transition_criteria", "page05_release_seal", "regression_snapshot")}
    return docs | manifests | release | pack


def _upstream_evidence_sources(root: Path, gates: tuple[dict[str, Any], ...]) -> list[tuple[str, str, dict[str, Any]]]:
    sources: list[tuple[str, str, dict[str, Any]]] = []
    for (stage, _, report_path, gate_path), gate in zip(PAGE05_UPSTREAM_STAGES, gates):
        report = _load_json(root / report_path) or {}
        gate_report = _load_json(root / gate_path) or gate
        sources.append((f"stage{stage}_report", report_path, report))
        sources.append((f"stage{stage}_gate", gate_path, gate_report))
    return sources


def _gate_or_existing(root: Path, report_name: str, runner) -> dict[str, Any]:
    path = root / "release/current" / report_name
    existing = _load_json(path)
    if isinstance(existing, dict):
        # Stage172 is a Page05 seal. Upstream Stage167~171 reports are sealed
        # evidence and must not be silently regenerated if they are blocked,
        # stale, or adversarially modified. Returning the current evidence lets
        # the Page05 stage-chain matrix fail closed instead of self-healing.
        return existing
    return runner(root)


def _stage_sealed(stage_chain: dict[str, Any], stage: str) -> bool:
    return any(item.get("stage") == stage and item.get("sealed") is True for item in stage_chain.get("stages", []))


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _payload_sha256(payload: Any) -> str:
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip().replace("\\", "/") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _is_forbidden_entry(entry: str) -> bool:
    return any(part in entry for part in ("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache")) or entry.endswith((".pyc", ".pyo"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode", "page", "page05_sealed", "page05_total_stage_count", "page05_release_checksum", "stage173_governance_contract_ready", "quality_channel_pass", "continuity_channel_pass", "regression_channel_pass", "boundary_channel_pass", "determinism_channel_pass", "provider_evaluation_enabled", "evaluation_write_enabled", "memory_write_enabled", "cross_project_write_enabled", "canon_mutation_enabled", "runtime_training_enabled", "auto_repair_apply_enabled", "provider_default_calls", "live_provider_call_count_in_release_gate", "provider_generation_count", "runtime_execution_count", "write_operation_count", "node2_raw_reveal_access", "boundary_violation_count", "credential_leakage", "branchpoint_lineage_preserved"
    )
    return {key: stage.get(key) for key in keep if key in stage}
