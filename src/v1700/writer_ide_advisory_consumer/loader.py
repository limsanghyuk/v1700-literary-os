from __future__ import annotations

from typing import Any


def validate_writer_ide_advisory_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []

    session = bundle.get("writer_session_record", {})
    cards = bundle.get("writer_ide_surface_cards", {}).get("cards", [])
    explanation = bundle.get("learnable_critic_explanation_record", {})
    warning = bundle.get("approval_boundary_warning", {})
    board = bundle.get("writer_ide_advisory_board", {})

    if not session.get("writer_session_id"):
        issues.append("missing_writer_session_id")
    if not session.get("work_id"):
        issues.append("missing_work_id")
    if not session.get("active_formula_signal_refs"):
        issues.append("missing_active_formula_signal_refs")
    if not session.get("active_corpus_refs"):
        issues.append("missing_active_corpus_refs")
    if not session.get("llm_boundary_level"):
        issues.append("missing_llm_boundary_level")

    work_ids = {str(card.get("work_id", "")) for card in cards if isinstance(card, dict)}
    if not cards:
        issues.append("surface_cards_empty")
    if len(work_ids) > 1:
        issues.append("mixed_work_ids_in_surface_cards")

    if any(card.get("advisory_only") is not True for card in cards if isinstance(card, dict)):
        issues.append("non_advisory_card_detected")
    if any(card.get("canonical_mutation_allowed") is not False for card in cards if isinstance(card, dict)):
        issues.append("surface_card_canonical_mutation_leak")

    if explanation.get("canonical_mutation_allowed") is not False:
        issues.append("learnable_critic_explanation_mutation_leak")
    if not explanation.get("advisory_output_id"):
        issues.append("missing_advisory_output_id")

    if warning.get("canonical_mutation_allowed") is not False:
        issues.append("approval_warning_mutation_leak")
    if not warning.get("required_contract_ref"):
        issues.append("missing_approval_contract_ref")

    required_zones = {"left", "center", "right"}
    card_zones = {str(card.get("zone", "")) for card in cards if isinstance(card, dict)}
    missing_zones = sorted(required_zones - card_zones)
    if missing_zones:
        issues.append(f"missing_board_zones:{','.join(missing_zones)}")

    if board.get("advisory_only") is not True:
        issues.append("board_not_advisory")
    if board.get("canonical_mutation_allowed") is not False:
        issues.append("board_canonical_mutation_leak")
    if not board.get("promotion_blockers"):
        issues.append("missing_promotion_blockers")

    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "surface_card_count": len(cards),
        "work_id_count": len(work_ids),
        "warning_count": len(board.get("warnings", [])) if isinstance(board.get("warnings"), list) else 0,
        "required_zones": sorted(required_zones),
        "card_zones": sorted(card_zones),
    }
