from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.generation_context_packet import build_generation_context_packet
from v1700.literary_generation_boundary.contracts import PAGE18_BOUNDARY_MODE
from v1700.output_capture_schema import build_canonical_mutation_blocker, build_output_capture_schema


def run_page18_generation_boundary_preflight(
    repo_root: Path | None = None,
    readiness_report: dict[str, Any] | None = None,
    policy_review: dict[str, Any] | None = None,
    opening_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build Page18 boundary records without opening runtime execution."""

    repo_root = repo_root or Path(__file__).resolve().parents[3]
    readiness_report = readiness_report or _load_json(repo_root / "release/current/page18_readiness_precheck_report.json") or {}
    policy_review = policy_review or _load_json(repo_root / "release/current/page18_policy_review_warning_decision.json") or {}
    opening_gate = opening_gate or _load_json(repo_root / "release/current/page18_opening_gate_checklist.json") or {}

    output_dir = repo_root / "release/current/literary_generation_boundary_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    work_id = _resolve_work_id(readiness_report)
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    metadata_refs = _build_metadata_refs(repo_root)
    proof_packet_refs = _build_proof_packet_refs(repo_root, readiness_report)
    context_packet = build_generation_context_packet(
        work_id,
        metadata_refs=metadata_refs,
        proof_packet_refs=proof_packet_refs,
    )
    provider_policy = _build_provider_execution_policy(work_id)
    output_schema = build_output_capture_schema(work_id)
    mutation_blocker = build_canonical_mutation_blocker(work_id)
    constraint_packet = _build_narrative_constraint_packet(work_id)
    request = _build_literary_generation_request(
        work_id=work_id,
        context_packet=context_packet,
        provider_policy=provider_policy,
        output_schema=output_schema,
        mutation_blocker=mutation_blocker,
        constraint_packet=constraint_packet,
    )
    validation = _validate_boundary(
        readiness_report=readiness_report,
        policy_review=policy_review,
        opening_gate=opening_gate,
        request=request,
        context_packet=context_packet,
        provider_policy=provider_policy,
        output_schema=output_schema,
        mutation_blocker=mutation_blocker,
    )
    boundary_report = _build_boundary_report(
        work_id=work_id,
        created_at=created_at,
        request=request,
        context_packet=context_packet,
        constraint_packet=constraint_packet,
        provider_policy=provider_policy,
        output_schema=output_schema,
        mutation_blocker=mutation_blocker,
        validation=validation,
    )

    result = {
        "title": "Page18 Controlled Literary Generation Boundary Preflight",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": PAGE18_BOUNDARY_MODE,
        "issues": list(validation["issues"]),
        "allowed_promotion": "page18_boundary_preflight_pass" if validation["status"] == "pass" else "blocked",
        "page18_runtime_opened": False,
        "stage243_created": False,
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "experiment_started": False,
        "output_capture_started": False,
        "paths": {
            "repo_root": str(repo_root),
            "output_dir": str(output_dir),
        },
        "parts": {
            "literary_generation_request": request,
            "generation_context_packet": context_packet,
            "narrative_constraint_packet": constraint_packet,
            "provider_execution_policy": provider_policy,
            "output_capture_schema": output_schema,
            "canonical_mutation_blocker": mutation_blocker,
            "page18_generation_boundary_validation_report": validation,
            "generation_boundary_report": boundary_report,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _resolve_work_id(readiness_report: dict[str, Any]) -> str:
    paths = readiness_report.get("paths", {}) if isinstance(readiness_report, dict) else {}
    if paths:
        return "10부"
    return "10부"


def _build_metadata_refs(repo_root: Path) -> list[dict[str, Any]]:
    candidates = [
        ("corpus_absorption_report", "release/current/corpus_ko_absorption_pack/corpus_absorption_report.json"),
        ("corpus_formula_bridge_report", "release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json"),
        ("formula_signal_store_report", "release/current/formula_signal_store_pack/formula_signal_store_report.json"),
        ("local_corpus_db_survey_report", "release/current/local_corpus_db_survey_report.json"),
        ("narrative_corpus_source_policy", "docs/policies/narrative_corpus_source_policy.md"),
        ("corpus_formula_signal_bridge_blueprint", "docs/architecture/corpus_formula_signal_bridge_blueprint.md"),
    ]
    return _build_existing_refs(repo_root, candidates, ref_class="metadata")


def _build_proof_packet_refs(repo_root: Path, readiness_report: dict[str, Any]) -> list[dict[str, Any]]:
    paths = readiness_report.get("paths", {}) if isinstance(readiness_report, dict) else {}
    candidates = [
        ("page18_readiness_precheck", "release/current/page18_readiness_precheck_report.json"),
        ("page18_policy_review_warning_decision", "release/current/page18_policy_review_warning_decision.json"),
        ("page18_opening_gate_checklist", "release/current/page18_opening_gate_checklist.json"),
        ("value_proof_guidance_report", paths.get("value_proof_guidance_report", "")),
        ("value_proof_preregistration_report", paths.get("value_proof_preregistration_report", "")),
        ("value_proof_blind_evaluator_report", paths.get("value_proof_blind_evaluator_report", "")),
        ("stage242_release_gate_report", "release/current/stage242_release_gate_report.json"),
        ("release_gate_report", "release/current/release_gate_report.json"),
    ]
    return _build_existing_refs(repo_root, candidates, ref_class="proof")


def _build_existing_refs(repo_root: Path, candidates: list[tuple[str, str]], *, ref_class: str) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for ref_id, relative_path in candidates:
        if not relative_path:
            continue
        path = repo_root / relative_path
        if not path.exists() or not path.is_file():
            continue
        refs.append(
            {
                "ref_id": ref_id,
                "ref_class": ref_class,
                "path": relative_path,
                "sha256": _sha256(path),
                "raw_text_exported": False,
            }
        )
    return refs


def _build_literary_generation_request(
    work_id: str,
    context_packet: dict[str, Any],
    provider_policy: dict[str, Any],
    output_schema: dict[str, Any],
    mutation_blocker: dict[str, Any],
    constraint_packet: dict[str, Any],
) -> dict[str, Any]:
    request = {
        "request_id": f"page18-literary-generation-request:{work_id}:preflight",
        "work_id": work_id,
        "mode": "boundary_preflight_only",
        "base_task_brief_ref": "value_proof_base_task_brief_placeholder",
        "target_length_policy": "locked_before_outputs",
        "genre_hint": "literary_series_scene_or_screenplay",
        "allowed_context_refs": [
            context_packet["context_packet_id"],
            constraint_packet["constraint_packet_id"],
        ],
        "forbidden_context_refs": [
            "source_text_payload",
            "unregistered_prompt_mutation",
            "post_output_threshold_change",
            "canonical_mutation",
        ],
        "provider_execution_policy_ref": provider_policy["policy_id"],
        "output_capture_schema_ref": output_schema["schema_id"],
        "canonical_mutation_blocker_ref": mutation_blocker["blocker_id"],
    }
    request["request_hash"] = _stable_hash(request)
    return request


def _build_narrative_constraint_packet(work_id: str) -> dict[str, Any]:
    packet = {
        "constraint_packet_id": f"page18-narrative-constraints:{work_id}:preflight",
        "work_id": work_id,
        "continuity_constraints": ["do_not_change_canonical_facts"],
        "character_arc_constraints": ["preserve_existing_arc_refs"],
        "conflict_progression_constraints": ["preserve_formula_signal_boundary"],
        "foreshadowing_constraints": ["advisory_only_until_output_capture_phase"],
        "style_boundary_refs": ["writer_advisory_surface_refs_only"],
    }
    packet["constraint_packet_hash"] = _stable_hash(packet)
    return packet


def _build_provider_execution_policy(work_id: str) -> dict[str, Any]:
    policy = {
        "policy_id": f"page18-provider-execution-policy:{work_id}:preflight",
        "work_id": work_id,
        "provider_default_calls": 0,
        "provider_generation_allowed": False,
        "credentials_externalized": True,
        "secret_logging_allowed": False,
        "requires_explicit_execution_phase": True,
        "runtime_training_enabled": False,
        "page18_runtime_opened": False,
    }
    policy["policy_hash"] = _stable_hash(policy)
    return policy


def _build_boundary_report(
    work_id: str,
    created_at: str,
    request: dict[str, Any],
    context_packet: dict[str, Any],
    constraint_packet: dict[str, Any],
    provider_policy: dict[str, Any],
    output_schema: dict[str, Any],
    mutation_blocker: dict[str, Any],
    validation: dict[str, Any],
) -> dict[str, Any]:
    report = {
        "boundary_report_id": f"page18-generation-boundary:{work_id}:preflight",
        "created_at": created_at,
        "work_id": work_id,
        "status": validation["status"],
        "request_hash": request.get("request_hash", ""),
        "context_packet_id": context_packet.get("context_packet_id", ""),
        "metadata_ref_count": len(context_packet.get("metadata_refs", [])),
        "proof_packet_ref_count": len(context_packet.get("proof_packet_refs", [])),
        "constraint_packet_hash": constraint_packet.get("constraint_packet_hash", ""),
        "provider_policy_hash": provider_policy.get("policy_hash", ""),
        "output_schema_id": output_schema.get("schema_id", ""),
        "mutation_blocker_id": mutation_blocker.get("blocker_id", ""),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "page18_runtime_opened": False,
        "stage243_created": False,
        "experiment_started": False,
        "output_capture_started": False,
        "source_text_allowed": False,
    }
    report["boundary_hash"] = _stable_hash(report)
    return report


def _validate_boundary(
    readiness_report: dict[str, Any],
    policy_review: dict[str, Any],
    opening_gate: dict[str, Any],
    request: dict[str, Any],
    context_packet: dict[str, Any],
    provider_policy: dict[str, Any],
    output_schema: dict[str, Any],
    mutation_blocker: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    if readiness_report.get("status") != "pass":
        issues.append("page18_readiness_not_pass")
    if readiness_report.get("decision") != "ready_for_policy_review":
        issues.append("page18_readiness_not_ready_for_policy_review")
    if policy_review.get("decision") != "warning_preserving_ready_for_page18_opening_gate":
        issues.append("policy_review_not_ready_for_opening_gate")
    if opening_gate.get("status") != "prepared_not_executed":
        issues.append("opening_gate_not_prepared")
    if provider_policy.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if provider_policy.get("provider_generation_allowed") is not False:
        issues.append("provider_generation_allowed")
    if output_schema.get("output_capture_started") is not False:
        issues.append("output_capture_started")
    if output_schema.get("capture_allowed") is not False:
        issues.append("capture_allowed")
    if mutation_blocker.get("canonical_mutation_allowed") is not False:
        issues.append("canonical_mutation_allowed")
    if context_packet.get("source_text_allowed") is not False:
        issues.append("source_text_allowed")
    if not context_packet.get("metadata_refs"):
        issues.append("metadata_refs_missing")
    if not context_packet.get("proof_packet_refs"):
        issues.append("proof_packet_refs_missing")
    forbidden_refs = set(request.get("forbidden_context_refs", []))
    if "source_text_payload" not in forbidden_refs:
        issues.append("source_text_payload_not_forbidden")
    if "unregistered_prompt_mutation" not in forbidden_refs:
        issues.append("unregistered_prompt_mutation_not_forbidden")
    return {"status": "pass" if not issues else "blocked", "issues": issues}


def _stable_hash(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_outputs(output_dir: Path, result: dict[str, Any]) -> None:
    parts = result["parts"]
    _write_json(output_dir / "literary_generation_request.json", parts["literary_generation_request"])
    _write_json(output_dir / "generation_context_packet.json", parts["generation_context_packet"])
    _write_json(output_dir / "narrative_constraint_packet.json", parts["narrative_constraint_packet"])
    _write_json(output_dir / "provider_execution_policy.json", parts["provider_execution_policy"])
    _write_json(output_dir / "output_capture_schema.json", parts["output_capture_schema"])
    _write_json(output_dir / "canonical_mutation_blocker.json", parts["canonical_mutation_blocker"])
    _write_json(output_dir / "page18_generation_boundary_validation_report.json", parts["page18_generation_boundary_validation_report"])
    _write_json(output_dir / "generation_boundary_report.json", parts["generation_boundary_report"])
    _write_json(output_dir / "page18_generation_boundary_preflight_report.json", result)
