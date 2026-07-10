from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.value_proof_arm_b_guidance_surface import run_value_proof_arm_b_guidance_surface

VALUE_PROOF_ARM_B_PREREGISTRATION_MODE = "VALUE_PROOF_ARM_B_PREREGISTRATION_PACKET_FIXTURE"


def run_value_proof_arm_b_preregistration_packet_builder(
    repo_root: Path | None = None,
    guidance_surface_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a preregistration packet from the Arm B guidance surface.

    This builder only creates locked metadata, hashes, and boundary records. It
    does not call providers, generate prose, run a Value Proof experiment, or
    open Page18 runtime.
    """

    repo_root = repo_root or Path(__file__).resolve().parents[3]
    guidance_surface_report = guidance_surface_report or _load_json(
        repo_root / "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json"
    ) or run_value_proof_arm_b_guidance_surface(repo_root=repo_root)

    output_dir = repo_root / "release/current/value_proof_arm_b_preregistration_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    counters = guidance_surface_report.get("counters", {})
    parts = guidance_surface_report.get("parts", {})
    work_id = str(counters.get("focus_work_id") or "UNKNOWN_WORK")
    guidance_cards = parts.get("value_proof_arm_b_guidance_cards", {}).get("cards", [])
    guidance_board = parts.get("value_proof_arm_b_guidance_board", {})

    arm_a_prompt_packet = _build_prompt_packet(
        arm="A",
        work_id=work_id,
        allowed_context=["base_task_brief", "target_length", "genre_hint"],
        forbidden_context=["formula_signal_refs", "writer_ide_surface_cards", "learnable_critic_explanation", "raw_script_text"],
    )
    arm_b_prompt_packet = _build_prompt_packet(
        arm="B",
        work_id=work_id,
        allowed_context=guidance_board.get("arm_b_allowed_context", []),
        forbidden_context=guidance_board.get("arm_b_forbidden_context", []),
        guidance_refs=[card.get("guidance_card_id") for card in guidance_cards],
        formula_signal_refs=guidance_board.get("preregistered_formula_signal_refs", []),
    )
    arm_config_registry = _build_arm_config_registry(work_id, arm_a_prompt_packet, arm_b_prompt_packet)
    lock_record = _build_preregistration_lock_record(work_id, created_at, arm_a_prompt_packet, arm_b_prompt_packet)
    validation = _validate_preregistration_packet(guidance_surface_report, arm_a_prompt_packet, arm_b_prompt_packet, lock_record)

    result = {
        "title": "Value Proof Arm B Preregistration Packet Builder",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": VALUE_PROOF_ARM_B_PREREGISTRATION_MODE,
        "issues": list(validation["issues"]),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "page18_runtime_opened": False,
        "experiment_started": False,
        "paths": {
            "repo_root": str(repo_root),
            "guidance_surface_report": str(
                repo_root / "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json"
            ),
        },
        "counters": {
            "focus_work_id": work_id,
            "arm_b_guidance_card_count": len(guidance_cards),
            "arm_count": 2,
            "prompt_packet_count": 2,
            "locked_threshold_count": len(lock_record["locked_thresholds"]),
        },
        "parts": {
            "arm_a_prompt_packet": arm_a_prompt_packet,
            "arm_b_prompt_packet": arm_b_prompt_packet,
            "arm_config_registry": arm_config_registry,
            "value_proof_preregistration_lock_record": lock_record,
            "value_proof_arm_b_preregistration_validation_report": validation,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _build_prompt_packet(
    arm: str,
    work_id: str,
    allowed_context: list[str],
    forbidden_context: list[str],
    guidance_refs: list[str | None] | None = None,
    formula_signal_refs: list[str] | None = None,
) -> dict[str, Any]:
    guidance_refs = [str(ref) for ref in (guidance_refs or []) if ref]
    formula_signal_refs = [str(ref) for ref in (formula_signal_refs or []) if ref]
    packet = {
        "prompt_packet_id": f"value-proof-arm-{arm.lower()}-prompt:{work_id}:preregistered",
        "arm": arm,
        "work_id": work_id,
        "base_task_brief_ref": "value_proof_base_task_brief_placeholder",
        "target_length_policy": "LOCKED_BEFORE_OUTPUTS",
        "allowed_context": list(allowed_context),
        "forbidden_context": list(forbidden_context),
        "guidance_refs": guidance_refs,
        "formula_signal_refs": formula_signal_refs,
        "visible_to_evaluator": False,
        "raw_script_text_allowed": False,
        "provider_generation_allowed": False,
        "canonical_mutation_allowed": False,
        "post_output_mutation_allowed": False,
    }
    packet["packet_hash"] = _stable_hash(packet)
    return packet


def _build_arm_config_registry(work_id: str, arm_a: dict[str, Any], arm_b: dict[str, Any]) -> dict[str, Any]:
    return {
        "registry_id": f"value-proof-arm-config:{work_id}:preregistered",
        "work_id": work_id,
        "arms": [
            {
                "arm": "A",
                "role": "PURE_LLM_BASELINE",
                "prompt_packet_id": arm_a["prompt_packet_id"],
                "prompt_packet_hash": arm_a["packet_hash"],
                "allowed_context": arm_a["allowed_context"],
                "forbidden_context": arm_a["forbidden_context"],
            },
            {
                "arm": "B",
                "role": "V1700_STRUCTURED_GUIDANCE",
                "prompt_packet_id": arm_b["prompt_packet_id"],
                "prompt_packet_hash": arm_b["packet_hash"],
                "allowed_context": arm_b["allowed_context"],
                "forbidden_context": arm_b["forbidden_context"],
            },
        ],
        "arm_labels_hidden_from_evaluator": True,
        "provider_execution_allowed": False,
    }


def _build_preregistration_lock_record(work_id: str, created_at: str, arm_a: dict[str, Any], arm_b: dict[str, Any]) -> dict[str, Any]:
    return {
        "lock_record_id": f"value-proof-preregistration-lock:{work_id}",
        "work_id": work_id,
        "created_at": created_at,
        "lock_status": "PREREGISTERED_PACKET_READY",
        "experiment_started": False,
        "locked_prompt_packet_hashes": {
            "A": arm_a["packet_hash"],
            "B": arm_b["packet_hash"],
        },
        "locked_thresholds": {
            "minimum_arm_b_preference_rate": "TBD_BEFORE_EXPERIMENT",
            "minimum_evaluator_count": "TBD_BEFORE_EXPERIMENT",
            "length_deviation_tolerance": "TBD_BEFORE_EXPERIMENT",
        },
        "locked_evaluator_policy": "BLIND_EVALUATION_REQUIRED",
        "blocked_until": [
            "thresholds_finalized",
            "arm_a_b_prompt_hashes_reviewed",
            "blind_evaluator_packet_built",
            "approval_boundary_reviewed",
        ],
        "page18_runtime_opened": False,
        "canonical_mutation_allowed": False,
    }


def _validate_preregistration_packet(
    guidance_surface_report: dict[str, Any],
    arm_a: dict[str, Any],
    arm_b: dict[str, Any],
    lock_record: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    if guidance_surface_report.get("status") != "pass":
        issues.append("guidance_surface_not_pass")
    if arm_a.get("arm") != "A" or arm_b.get("arm") != "B":
        issues.append("arm_labels_invalid")
    if not arm_a.get("packet_hash") or not arm_b.get("packet_hash"):
        issues.append("prompt_packet_hash_missing")
    if arm_a.get("packet_hash") == arm_b.get("packet_hash"):
        issues.append("arm_prompt_hashes_identical")
    if arm_b.get("raw_script_text_allowed") is not False:
        issues.append("arm_b_allows_raw_script_text")
    if arm_b.get("provider_generation_allowed") is not False:
        issues.append("arm_b_allows_provider_generation")
    if lock_record.get("experiment_started") is not False:
        issues.append("experiment_started_before_lock_review")
    if lock_record.get("page18_runtime_opened") is not False:
        issues.append("page18_runtime_opened")
    return {"status": "pass" if not issues else "blocked", "issues": issues}


def _stable_hash(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_outputs(output_dir: Path, result: dict[str, Any]) -> None:
    parts = result["parts"]
    _write_json(output_dir / "arm_a_prompt_packet.json", parts["arm_a_prompt_packet"])
    _write_json(output_dir / "arm_b_prompt_packet.json", parts["arm_b_prompt_packet"])
    _write_json(output_dir / "arm_config_registry.json", parts["arm_config_registry"])
    _write_json(output_dir / "value_proof_preregistration_lock_record.json", parts["value_proof_preregistration_lock_record"])
    _write_json(output_dir / "value_proof_arm_b_preregistration_validation_report.json", parts["value_proof_arm_b_preregistration_validation_report"])
    _write_json(output_dir / "value_proof_arm_b_preregistration_packet_report.json", result)
