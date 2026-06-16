from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.writer_ide_advisory_consumer import run_writer_ide_advisory_consumer

VALUE_PROOF_ARM_B_GUIDANCE_MODE = "VALUE_PROOF_ARM_B_GUIDANCE_SURFACE_FIXTURE"


def run_value_proof_arm_b_guidance_surface(
    repo_root: Path | None = None,
    writer_ide_advisory_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an advisory-only Value Proof Arm B guidance surface.

    The surface consumes the Writer IDE advisory consumer report and projects a
    preregistration-safe guidance pack for Arm B. It does not call providers,
    generate prose, mutate canonical records, or open Page18 runtime.
    """

    repo_root = repo_root or Path(__file__).resolve().parents[3]
    writer_ide_advisory_report = writer_ide_advisory_report or _load_json(
        repo_root / "release/current/writer_ide_advisory_pack/writer_ide_advisory_consumer_report.json"
    ) or run_writer_ide_advisory_consumer(repo_root=repo_root)

    output_dir = repo_root / "release/current/value_proof_arm_b_guidance_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    counters = writer_ide_advisory_report.get("counters", {})
    parts = writer_ide_advisory_report.get("parts", {})
    work_id = str(counters.get("focus_work_id") or parts.get("writer_session_record", {}).get("work_id") or "UNKNOWN_WORK")
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    surface_cards = parts.get("writer_ide_surface_cards", {}).get("cards", [])
    arm_b_cards = _build_arm_b_guidance_cards(work_id, surface_cards)
    warning = _build_preregistration_warning(work_id)
    board = _build_board(work_id, arm_b_cards, warning, created_at)
    validation = _validate_guidance_surface(arm_b_cards, warning, board)

    result = {
        "title": "Value Proof Arm B Guidance Surface",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": VALUE_PROOF_ARM_B_GUIDANCE_MODE,
        "issues": list(validation["issues"]),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "advisory_only": True,
        "page18_runtime_opened": False,
        "paths": {
            "repo_root": str(repo_root),
            "writer_ide_advisory_consumer_report": str(
                repo_root / "release/current/writer_ide_advisory_pack/writer_ide_advisory_consumer_report.json"
            ),
        },
        "counters": {
            "focus_work_id": work_id,
            "arm_b_guidance_card_count": len(arm_b_cards),
            "source_surface_card_count": len(surface_cards),
            "promotion_blocker_count": len(board["promotion_blockers"]),
        },
        "parts": {
            "value_proof_arm_b_guidance_cards": {
                "status": "pass" if arm_b_cards else "blocked",
                "work_id": work_id,
                "card_count": len(arm_b_cards),
                "cards": arm_b_cards,
            },
            "value_proof_preregistration_warning": warning,
            "value_proof_arm_b_guidance_board": board,
            "value_proof_arm_b_guidance_validation_report": validation,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _build_arm_b_guidance_cards(work_id: str, surface_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for card in surface_cards:
        if str(card.get("work_id", "")) != work_id:
            continue
        signal_refs = [str(ref) for ref in card.get("signal_refs", []) if str(ref)]
        if not signal_refs:
            continue
        prereg_ready = str(card.get("review_status", "")) == "VALID_FOR_VALUE_PROOF_PREREGISTRATION"
        zone = str(card.get("zone", "center"))
        guidance_type = "arm_b_formula_guidance" if prereg_ready else "arm_b_context_boundary"
        cards.append(
            {
                "guidance_card_id": f"value-proof-arm-b:{zone}:{len(cards) + 1}:{work_id}",
                "source_card_id": str(card.get("card_id", "")),
                "work_id": work_id,
                "zone": zone,
                "headline": str(card.get("headline", "")),
                "guidance_summary": str(card.get("summary", "")),
                "guidance_type": guidance_type,
                "signal_refs": signal_refs,
                "confidence": round(float(card.get("confidence") or 0.0), 6),
                "allowed_arm": "B_ONLY_PREREGISTERED_GUIDANCE",
                "visible_to_evaluator": False,
                "advisory_only": True,
                "canonical_mutation_allowed": False,
                "prompt_mutation_allowed_after_preregistration": False,
                "requires_preregistration": True,
            }
        )
    return cards


def _build_preregistration_warning(work_id: str) -> dict[str, Any]:
    return {
        "warning_id": f"value-proof-arm-b-warning:{work_id}:preregistration",
        "work_id": work_id,
        "warning_type": "PREREGISTRATION_REQUIRED_BEFORE_ARM_B_USE",
        "message": "Arm B guidance may only be used after prompt packets, thresholds, evaluator policy, and allowed formula guidance are preregistered.",
        "required_contract_refs": [
            "docs/templates/value_proof_preregistration_template.md",
            "docs/fixtures/value_proof_minimum_fixture_spec.md",
            "docs/architecture/value_proof_experiment_engine_blueprint.md",
        ],
        "canonical_mutation_allowed": False,
        "provider_generation_allowed": False,
        "page18_runtime_opened": False,
    }


def _build_board(work_id: str, cards: list[dict[str, Any]], warning: dict[str, Any], created_at: str) -> dict[str, Any]:
    preregistered_formula_signal_refs = sorted({ref for card in cards for ref in card["signal_refs"]})
    return {
        "board_id": f"value-proof-arm-b-board:{work_id}:guidance",
        "work_id": work_id,
        "created_at": created_at,
        "guidance_surface_status": "READY_FOR_PREREGISTRATION" if cards else "BLOCKED_NO_GUIDANCE_CARDS",
        "advisory_only": True,
        "canonical_mutation_allowed": False,
        "provider_generation_allowed": False,
        "visible_to_evaluator": False,
        "arm": "B",
        "arm_b_allowed_context": [
            "metadata_only_corpus_refs",
            "writer_ide_advisory_surface_cards",
            "formula_signal_refs",
            "learnable_critic_review_only_explanation",
        ],
        "arm_b_forbidden_context": [
            "raw_script_text",
            "unregistered_prompt_mutation",
            "post_output_threshold_change",
            "canonical_mutation",
            "evaluator_visible_arm_label",
        ],
        "preregistered_formula_signal_refs": preregistered_formula_signal_refs,
        "guidance_card_count": len(cards),
        "promotion_blockers": [
            "value_proof_preregistration_required",
            "arm_a_b_prompt_hash_required",
            "blind_evaluator_packet_required",
            "approval_boundary_required",
        ],
        "warnings": [warning],
        "cards": cards,
    }


def _validate_guidance_surface(cards: list[dict[str, Any]], warning: dict[str, Any], board: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if not cards:
        issues.append("arm_b_guidance_cards_empty")
    if warning.get("canonical_mutation_allowed") is not False:
        issues.append("warning_allows_canonical_mutation")
    if board.get("visible_to_evaluator") is not False:
        issues.append("board_visible_to_evaluator")
    if board.get("canonical_mutation_allowed") is not False:
        issues.append("board_allows_canonical_mutation")
    if not board.get("promotion_blockers"):
        issues.append("promotion_blockers_missing")
    work_ids = {card.get("work_id") for card in cards}
    if len(work_ids) > 1:
        issues.append("mixed_work_guidance_surface")
    if any(card.get("requires_preregistration") is not True for card in cards):
        issues.append("card_missing_preregistration_requirement")
    if any(card.get("advisory_only") is not True for card in cards):
        issues.append("card_not_advisory_only")
    if any(card.get("canonical_mutation_allowed") is not False for card in cards):
        issues.append("card_allows_canonical_mutation")
    return {"status": "pass" if not issues else "blocked", "issues": issues}


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_outputs(output_dir: Path, result: dict[str, Any]) -> None:
    parts = result["parts"]
    _write_json(output_dir / "value_proof_arm_b_guidance_cards.json", parts["value_proof_arm_b_guidance_cards"])
    _write_json(output_dir / "value_proof_preregistration_warning.json", parts["value_proof_preregistration_warning"])
    _write_json(output_dir / "value_proof_arm_b_guidance_board.json", parts["value_proof_arm_b_guidance_board"])
    _write_json(output_dir / "value_proof_arm_b_guidance_validation_report.json", parts["value_proof_arm_b_guidance_validation_report"])
    _write_json(output_dir / "value_proof_arm_b_guidance_surface_report.json", result)
