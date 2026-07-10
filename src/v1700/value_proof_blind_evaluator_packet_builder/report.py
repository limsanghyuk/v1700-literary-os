from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.value_proof_arm_b_preregistration_packet_builder import (
    run_value_proof_arm_b_preregistration_packet_builder,
)

VALUE_PROOF_BLIND_EVALUATOR_MODE = "VALUE_PROOF_BLIND_EVALUATOR_PACKET_FIXTURE"


def run_value_proof_blind_evaluator_packet_builder(
    repo_root: Path | None = None,
    preregistration_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build evaluator-facing packet metadata while hiding arm labels.

    This builder does not execute an experiment, call a provider, capture model
    output, open Page18, train, or mutate canonical records. It only prepares
    packet metadata and a private mapping for later review.
    """

    repo_root = repo_root or Path(__file__).resolve().parents[3]
    preregistration_report = preregistration_report or _load_json(
        repo_root / "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json"
    ) or run_value_proof_arm_b_preregistration_packet_builder(repo_root=repo_root)

    output_dir = repo_root / "release/current/value_proof_blind_evaluator_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    parts = preregistration_report.get("parts", {})
    arm_a = parts.get("arm_a_prompt_packet", {})
    arm_b = parts.get("arm_b_prompt_packet", {})
    lock_record = parts.get("value_proof_preregistration_lock_record", {})
    work_id = str(preregistration_report.get("counters", {}).get("focus_work_id") or lock_record.get("work_id") or "UNKNOWN_WORK")

    packet_01 = _build_evaluator_packet(slot="slot_01", work_id=work_id, prompt_packet=arm_a)
    packet_02 = _build_evaluator_packet(slot="slot_02", work_id=work_id, prompt_packet=arm_b)
    packet_registry = _build_packet_registry(work_id, created_at, packet_01, packet_02)
    private_mapping = _build_private_mapping(work_id, arm_a, arm_b, packet_01, packet_02)
    boundary = _build_boundary_report(work_id, packet_registry, private_mapping)
    validation = _validate_blind_packet(preregistration_report, packet_01, packet_02, private_mapping, boundary)

    result = {
        "title": "Value Proof Blind Evaluator Packet Builder",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": VALUE_PROOF_BLIND_EVALUATOR_MODE,
        "issues": list(validation["issues"]),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "page18_runtime_opened": False,
        "experiment_started": False,
        "output_capture_started": False,
        "paths": {
            "repo_root": str(repo_root),
            "preregistration_report": str(
                repo_root / "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json"
            ),
        },
        "counters": {
            "focus_work_id": work_id,
            "evaluator_packet_count": 2,
            "private_mapping_count": 2,
            "public_arm_label_count": 0,
        },
        "parts": {
            "blind_packet_registry": packet_registry,
            "evaluator_packet_01": packet_01,
            "evaluator_packet_02": packet_02,
            "private_arm_mapping": private_mapping,
            "blind_evaluator_boundary_report": boundary,
            "value_proof_blind_evaluator_validation_report": validation,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _build_evaluator_packet(slot: str, work_id: str, prompt_packet: dict[str, Any]) -> dict[str, Any]:
    prompt_packet_id = str(prompt_packet.get("prompt_packet_id", ""))
    prompt_packet_hash = str(prompt_packet.get("packet_hash", ""))
    packet = {
        "evaluator_packet_id": f"value-proof-evaluator-packet:{work_id}:{slot}",
        "slot": slot,
        "work_id": work_id,
        "source_prompt_packet_ref_hash": _prompt_packet_ref_hash(prompt_packet_id, prompt_packet_hash),
        "visible_to_evaluator": True,
        "label_visible_to_evaluator": False,
        "evaluation_prompt_body_included": False,
        "output_capture_allowed": False,
        "provider_generation_allowed": False,
        "canonical_mutation_allowed": False,
        "raw_script_text_allowed": False,
        "evaluator_instructions": [
            "Compare only the later captured outputs.",
            "Do not infer the hidden packet source.",
            "Do not change thresholds after outputs are seen.",
        ],
    }
    packet["evaluator_packet_hash"] = _stable_hash(packet)
    return packet


def _prompt_packet_ref_hash(prompt_packet_id: str, prompt_packet_hash: str) -> str:
    if not prompt_packet_id or not prompt_packet_hash:
        return ""
    return _stable_hash(
        {
            "source_prompt_packet_id": prompt_packet_id,
            "source_prompt_packet_hash": prompt_packet_hash,
        }
    )


def _build_packet_registry(work_id: str, created_at: str, packet_01: dict[str, Any], packet_02: dict[str, Any]) -> dict[str, Any]:
    registry = {
        "registry_id": f"value-proof-blind-evaluator-registry:{work_id}",
        "work_id": work_id,
        "created_at": created_at,
        "blind_slots": [
            {
                "slot": packet_01["slot"],
                "evaluator_packet_id": packet_01["evaluator_packet_id"],
                "evaluator_packet_hash": packet_01["evaluator_packet_hash"],
            },
            {
                "slot": packet_02["slot"],
                "evaluator_packet_id": packet_02["evaluator_packet_id"],
                "evaluator_packet_hash": packet_02["evaluator_packet_hash"],
            },
        ],
        "arm_labels_visible_to_evaluator": False,
        "output_capture_started": False,
    }
    registry["registry_hash"] = _stable_hash(registry)
    return registry


def _build_private_mapping(
    work_id: str,
    arm_a: dict[str, Any],
    arm_b: dict[str, Any],
    packet_01: dict[str, Any],
    packet_02: dict[str, Any],
) -> dict[str, Any]:
    mapping = {
        "mapping_id": f"value-proof-private-arm-mapping:{work_id}",
        "work_id": work_id,
        "visible_to_evaluator": False,
        "records": [
            {
                "slot": packet_01["slot"],
                "arm": arm_a.get("arm", "A"),
                "prompt_packet_hash": arm_a.get("packet_hash", ""),
                "evaluator_packet_hash": packet_01["evaluator_packet_hash"],
            },
            {
                "slot": packet_02["slot"],
                "arm": arm_b.get("arm", "B"),
                "prompt_packet_hash": arm_b.get("packet_hash", ""),
                "evaluator_packet_hash": packet_02["evaluator_packet_hash"],
            },
        ],
    }
    mapping["mapping_hash"] = _stable_hash(mapping)
    return mapping


def _build_boundary_report(work_id: str, registry: dict[str, Any], private_mapping: dict[str, Any]) -> dict[str, Any]:
    return {
        "boundary_report_id": f"value-proof-blind-evaluator-boundary:{work_id}",
        "work_id": work_id,
        "registry_hash": registry.get("registry_hash", ""),
        "private_mapping_hash": private_mapping.get("mapping_hash", ""),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "page18_runtime_opened": False,
        "experiment_started": False,
        "output_capture_started": False,
        "arm_labels_visible_to_evaluator": False,
        "raw_script_text_allowed": False,
    }


def _validate_blind_packet(
    preregistration_report: dict[str, Any],
    packet_01: dict[str, Any],
    packet_02: dict[str, Any],
    private_mapping: dict[str, Any],
    boundary: dict[str, Any],
) -> dict[str, Any]:
    issues: list[str] = []
    if preregistration_report.get("status") != "pass":
        issues.append("preregistration_report_not_pass")
    if not packet_01.get("source_prompt_packet_ref_hash") or not packet_02.get("source_prompt_packet_ref_hash"):
        issues.append("source_prompt_packet_ref_hash_missing")
    if packet_01.get("evaluator_packet_hash") == packet_02.get("evaluator_packet_hash"):
        issues.append("evaluator_packet_hashes_identical")
    if packet_01.get("label_visible_to_evaluator") is not False or packet_02.get("label_visible_to_evaluator") is not False:
        issues.append("arm_label_visible_to_evaluator")
    if private_mapping.get("visible_to_evaluator") is not False:
        issues.append("private_mapping_visible_to_evaluator")
    if boundary.get("provider_default_calls") != 0:
        issues.append("provider_call_detected")
    if boundary.get("experiment_started") is not False:
        issues.append("experiment_started")
    if boundary.get("output_capture_started") is not False:
        issues.append("output_capture_started")
    if boundary.get("page18_runtime_opened") is not False:
        issues.append("page18_runtime_opened")
    if boundary.get("canonical_mutation_allowed") is not False:
        issues.append("canonical_mutation_allowed")
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
    _write_json(output_dir / "blind_packet_registry.json", parts["blind_packet_registry"])
    _write_json(output_dir / "evaluator_packet_01.json", parts["evaluator_packet_01"])
    _write_json(output_dir / "evaluator_packet_02.json", parts["evaluator_packet_02"])
    _write_json(output_dir / "private_arm_mapping.json", parts["private_arm_mapping"])
    _write_json(output_dir / "blind_evaluator_boundary_report.json", parts["blind_evaluator_boundary_report"])
    _write_json(output_dir / "value_proof_blind_evaluator_validation_report.json", parts["value_proof_blind_evaluator_validation_report"])
    _write_json(output_dir / "value_proof_blind_evaluator_packet_report.json", result)
