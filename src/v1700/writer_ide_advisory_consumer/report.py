from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.formula_signal_store import run_formula_signal_store
from v1700.formula_signal_store.loader import load_formula_signal_registry, work_id_from_signal
from v1700.learnable_critic_audit import run_learnable_critic_audit_fixture

from .contracts import (
    ApprovalBoundaryWarning,
    LearnableCriticExplanationRecord,
    WriterIdeAdvisoryBoard,
    WriterIdeSurfaceCard,
    WriterSessionRecord,
)
from .loader import validate_writer_ide_advisory_bundle

WRITER_IDE_ADVISORY_CONSUMER_MODE = "WRITER_IDE_ADVISORY_CONSUMER_FIXTURE"


def run_writer_ide_advisory_consumer(
    repo_root: Path | None = None,
    formula_signal_store_report: dict[str, Any] | None = None,
    learnable_critic_audit_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    formula_signal_store_report = formula_signal_store_report or _load_existing_report(
        repo_root / "release/current/formula_signal_store_pack/formula_signal_store_report.json"
    ) or run_formula_signal_store(repo_root=repo_root)
    learnable_critic_audit_report = learnable_critic_audit_report or _load_existing_report(
        repo_root / "release/current/learnable_critic_audit_pack/learnable_critic_audit_report.json"
    ) or run_learnable_critic_audit_fixture(repo_root=repo_root, formula_signal_store_report=formula_signal_store_report)

    output_dir = repo_root / "release/current/writer_ide_advisory_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_signal = learnable_critic_audit_report.get("parts", {}).get("selected_formula_signal", {})
    work_id = _signal_work_id(selected_signal) or _first_work_id_from_cards(formula_signal_store_report)
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    registry = _load_signal_registry(repo_root, formula_signal_store_report)
    card_payload = formula_signal_store_report.get("parts", {}).get("writer_ide_advisory_cards", {})
    source_cards = card_payload.get("cards", []) if isinstance(card_payload, dict) else []
    focus_cards = _build_surface_cards(source_cards, registry, work_id, learnable_critic_audit_report)

    audit_parts = learnable_critic_audit_report.get("parts", {})
    critic_input_source = audit_parts.get("critic_input_source_record", {})
    advisory_output = audit_parts.get("advisory_output_record", {})
    approval = audit_parts.get("human_approval_record", {})
    diff = audit_parts.get("coefficient_diff_record", {})
    alignment = audit_parts.get("alignment_result_record", {})
    config = audit_parts.get("learnable_critic_config", {})

    corpus_refs = tuple(
        sorted(
            {
                str(signal_ref)
                for card in focus_cards
                if "corpus_reference" in card.panel_ref
                for signal_ref in card.signal_refs
            }
        )
    )
    if not corpus_refs and critic_input_source.get("corpus_signal_ref"):
        corpus_refs = (str(critic_input_source["corpus_signal_ref"]),)

    writer_session = WriterSessionRecord(
        writer_session_id=f"writer-session:{work_id}:critic-review",
        work_id=work_id,
        session_scope="LEARNABLE_CRITIC_REVIEW",
        active_scene_refs=(f"scene:advisory-focus:{work_id}",),
        active_character_refs=(),
        active_corpus_refs=corpus_refs,
        active_formula_signal_refs=tuple(sorted({signal_ref for card in focus_cards for signal_ref in card.signal_refs})),
        active_agent_refs=(str(config.get("critic_id", "critic:unknown")),),
        llm_boundary_level="LLM-0",
        started_at=created_at,
        ended_at=created_at,
        session_status="LOCKED_FOR_REVIEW",
    )

    explanation = LearnableCriticExplanationRecord(
        explanation_record_id=f"critic-explanation:{work_id}:review",
        writer_session_id=writer_session.writer_session_id,
        critic_id=str(config.get("critic_id", "critic:unknown")),
        advisory_output_id=str(advisory_output.get("advisory_output_id", "")),
        formula_signal_ref=str(critic_input_source.get("formula_signal_ref", "")),
        coefficient_diff_id=str(diff.get("coefficient_diff_id", "")),
        alignment_result_id=str(alignment.get("alignment_result_id", "")),
        confidence=round(float(advisory_output.get("confidence") or 0.0), 6),
        explanation_summary=str(advisory_output.get("explanation", "")),
        suggested_action=str(advisory_output.get("suggested_action", "")),
        approval_status=str(approval.get("approval_status", "")),
        canonical_mutation_allowed=False,
    )

    warning = ApprovalBoundaryWarning(
        warning_id=f"approval-warning:{work_id}:critic-output",
        writer_session_id=writer_session.writer_session_id,
        subject_record_id=str(advisory_output.get("advisory_output_id", "")),
        subject_record_type="LearnableCriticAdvisoryOutputRecord",
        warning_type="APPROVAL_REQUIRED_BEFORE_CANONICAL_MUTATION",
        message="LearnableCritic output may be shown to the writer, but canonical manuscript mutation remains blocked until an ApprovalDecisionRecord is created.",
        required_contract_ref="docs/contracts/approval_decision_record_contract.md",
        approval_status=str(approval.get("approval_status", "")),
        canonical_mutation_allowed=False,
    )

    board = WriterIdeAdvisoryBoard(
        board_id=f"writer-board:{work_id}:advisory-review",
        writer_session_id=writer_session.writer_session_id,
        work_id=work_id,
        advisory_only=True,
        canonical_mutation_allowed=False,
        panel_refs=tuple(sorted({card.panel_ref for card in focus_cards})),
        promotion_blockers=(
            "approval_decision_required",
            "scene_diff_required_for_canonical_change",
            "learnable_critic_output_remains_advisory",
        ),
        cards=tuple(focus_cards),
        warnings=(warning,),
    )

    bundle = {
        "writer_session_record": writer_session.to_dict(),
        "learnable_critic_explanation_record": explanation.to_dict(),
        "approval_boundary_warning": warning.to_dict(),
        "writer_ide_surface_cards": {
            "status": "pass" if focus_cards else "blocked",
            "issues": [] if focus_cards else ["focus_cards_empty"],
            "work_id": work_id,
            "card_count": len(focus_cards),
            "cards": [card.to_dict() for card in focus_cards],
        },
        "writer_ide_advisory_board": board.to_dict(),
    }
    validation = validate_writer_ide_advisory_bundle(bundle)

    result = {
        "title": "Writer IDE Advisory Consumer",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": WRITER_IDE_ADVISORY_CONSUMER_MODE,
        "issues": list(validation["issues"]),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "advisory_only": True,
        "paths": {
            "repo_root": str(repo_root),
            "formula_signal_store_report": str(repo_root / "release/current/formula_signal_store_pack/formula_signal_store_report.json"),
            "learnable_critic_audit_report": str(repo_root / "release/current/learnable_critic_audit_pack/learnable_critic_audit_report.json"),
        },
        "counters": {
            "focus_work_id": work_id,
            "surface_card_count": len(focus_cards),
            "signal_ref_count": len(writer_session.active_formula_signal_refs),
            "corpus_ref_count": len(writer_session.active_corpus_refs),
            "promotion_blocker_count": len(board.promotion_blockers),
        },
        "parts": {
            **bundle,
            "writer_ide_advisory_validation_report": validation,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _build_surface_cards(
    source_cards: list[dict[str, Any]],
    registry: list[dict[str, Any]],
    work_id: str,
    learnable_critic_audit_report: dict[str, Any],
) -> list[WriterIdeSurfaceCard]:
    registry_map = {str(record.get("formula_signal_id", "")): record for record in registry}
    cards_for_work = [card for card in source_cards if str(card.get("work_id", "")) == work_id]
    visible_cards: list[WriterIdeSurfaceCard] = []
    seen_panels: set[str] = set()

    for card in cards_for_work:
        panel_ref = str(card.get("panel_ref", ""))
        if panel_ref in seen_panels:
            continue
        signals = [registry_map.get(str(signal_ref), {}) for signal_ref in card.get("signal_refs", [])]
        top_signal = sorted(signals, key=lambda item: float(item.get("confidence") or 0.0), reverse=True)[0] if signals else {}
        visible_cards.append(
            WriterIdeSurfaceCard(
                card_id=str(card.get("card_id", "")),
                panel_ref=panel_ref,
                zone=_panel_zone(panel_ref),
                work_id=work_id,
                headline=str(card.get("headline", "")),
                summary=_surface_summary(card, top_signal),
                severity=str(card.get("severity", "advisory")),
                formula_group_badges=tuple(str(badge) for badge in card.get("badges", [])),
                signal_refs=tuple(str(signal_ref) for signal_ref in card.get("signal_refs", [])),
                confidence=round(float(top_signal.get("confidence") or 0.0), 6),
                advisory_only=True,
                canonical_mutation_allowed=False,
                review_status=str(top_signal.get("review_status", "VALID_FOR_UI_WIRING")),
            )
        )
        seen_panels.add(panel_ref)

    visible_cards.append(_build_center_review_card(work_id, learnable_critic_audit_report))
    return sorted(visible_cards, key=lambda item: (item.zone, item.panel_ref, item.card_id))


def _build_center_review_card(work_id: str, learnable_critic_audit_report: dict[str, Any]) -> WriterIdeSurfaceCard:
    audit_parts = learnable_critic_audit_report.get("parts", {})
    advisory_output = audit_parts.get("advisory_output_record", {})
    alignment = audit_parts.get("alignment_result_record", {})
    approval = audit_parts.get("human_approval_record", {})

    summary = (
        f"{advisory_output.get('score_or_label', 'REVIEW_ONLY')} | "
        f"delta={alignment.get('improvement_delta', 0.0)} | "
        f"approval={approval.get('approval_status', 'PENDING_REVIEW')}"
    )
    return WriterIdeSurfaceCard(
        card_id=f"writer-card:writer_ide:center_panel:approval_boundary:{work_id}",
        panel_ref="writer_ide:center_panel:approval_boundary",
        zone="center",
        work_id=work_id,
        headline=f"{work_id} approval boundary review",
        summary=summary,
        severity="review",
        formula_group_badges=("LearnableCritic", "Approval Boundary"),
        signal_refs=(str(audit_parts.get("critic_input_source_record", {}).get("formula_signal_ref", "")),),
        confidence=round(float(advisory_output.get("confidence") or 0.0), 6),
        advisory_only=True,
        canonical_mutation_allowed=False,
        review_status=str(approval.get("approval_status", "PENDING_REVIEW")),
    )


def _surface_summary(card: dict[str, Any], signal: dict[str, Any]) -> str:
    label = str(signal.get("output_signal_value_or_label", "")).strip()
    explanation = str(signal.get("explanation_summary", "")).strip()
    if label and explanation:
        return f"{label} | {explanation}"
    if label:
        return label
    return str(card.get("summary", ""))


def _panel_zone(panel_ref: str) -> str:
    if ":left_panel:" in panel_ref:
        return "left"
    if ":right_panel:" in panel_ref:
        return "right"
    return "center"


def _signal_work_id(signal: dict[str, Any]) -> str:
    explicit = str(signal.get("work_id", "")).strip()
    if explicit:
        return explicit
    derived = work_id_from_signal(signal)
    if derived:
        return derived
    signal_id = str(signal.get("formula_signal_id", ""))
    return signal_id.rsplit(":", 1)[-1] if ":" in signal_id else ""


def _first_work_id_from_cards(formula_signal_store_report: dict[str, Any]) -> str:
    cards = formula_signal_store_report.get("parts", {}).get("writer_ide_advisory_cards", {}).get("cards", [])
    for card in cards:
        work_id = str(card.get("work_id", "")).strip()
        if work_id:
            return work_id
    return "unknown_work"


def _load_signal_registry(repo_root: Path, formula_signal_store_report: dict[str, Any]) -> list[dict[str, Any]]:
    registry_path_str = formula_signal_store_report.get("paths", {}).get(
        "source_registry", str(repo_root / "release/current/corpus_formula_bridge_pack/formula_signal_registry.json")
    )
    registry_path = Path(registry_path_str)
    if not registry_path.is_absolute():
        registry_path = repo_root / registry_path
    return load_formula_signal_registry(registry_path)


def _load_existing_report(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_outputs(output_dir: Path, payload: dict[str, Any]) -> None:
    parts = payload["parts"]
    _write_json(output_dir / "writer_session_record.json", parts["writer_session_record"])
    _write_json(output_dir / "learnable_critic_explanation_record.json", parts["learnable_critic_explanation_record"])
    _write_json(output_dir / "approval_boundary_warning.json", parts["approval_boundary_warning"])
    _write_json(output_dir / "writer_ide_surface_cards.json", parts["writer_ide_surface_cards"])
    _write_json(output_dir / "writer_ide_advisory_board.json", parts["writer_ide_advisory_board"])
    _write_json(output_dir / "writer_ide_advisory_validation_report.json", parts["writer_ide_advisory_validation_report"])
    _write_json(output_dir / "writer_ide_advisory_consumer_report.json", payload)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
