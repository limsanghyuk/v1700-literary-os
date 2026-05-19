from __future__ import annotations

from typing import Any

from .contracts import ContradictionClassification, ContradictionEvidence


def build_stage132_fixture_evidence() -> tuple[ContradictionEvidence, ...]:
    return (
        ContradictionEvidence(
            case_id="CEX-TRUE-001",
            surface_conflict=True,
            canon_fact_a="Work A says the mentor died in 1999.",
            canon_fact_b="Work B says the same mentor appears alive in 2003.",
            same_canon_scope=True,
            truth_confidence_a=0.94,
            truth_confidence_b=0.92,
        ),
        ContradictionEvidence(
            case_id="CEX-MYST-001",
            surface_conflict=True,
            canon_fact_a="The witness says the letter was burned.",
            canon_fact_b="A locked reveal says the letter survived.",
            same_canon_scope=True,
            truth_confidence_a=0.62,
            truth_confidence_b=0.91,
            reveal_lock_id="RL-EP08-LETTER",
            payoff_budget_reserved=True,
            writer_intent_tag="intentional_mystery",
        ),
        ContradictionEvidence(
            case_id="CEX-POV-001",
            surface_conflict=True,
            canon_fact_a="A character believes the doctor betrayed the team.",
            canon_fact_b="The canon ledger says the doctor protected the team.",
            same_canon_scope=False,
            truth_confidence_a=0.55,
            truth_confidence_b=0.90,
            pov_boundary=True,
            writer_intent_tag="character_misunderstanding",
        ),
        ContradictionEvidence(
            case_id="CEX-DELAY-001",
            surface_conflict=True,
            canon_fact_a="Episode 3 implies the father abandoned the family.",
            canon_fact_b="Episode 9 reveal says the father was coerced.",
            same_canon_scope=True,
            truth_confidence_a=0.67,
            truth_confidence_b=0.88,
            scheduled_reveal_episode=9,
            payoff_budget_reserved=True,
            writer_intent_tag="reveal_delay",
        ),
        ContradictionEvidence(
            case_id="CEX-CLEAR-001",
            surface_conflict=False,
            canon_fact_a="The nurse hides the ring.",
            canon_fact_b="The ring is missing in the next scene.",
            same_canon_scope=True,
            truth_confidence_a=0.91,
            truth_confidence_b=0.91,
        ),
    )


def classify_contradiction(evidence: ContradictionEvidence) -> ContradictionClassification:
    if not evidence.surface_conflict:
        return ContradictionClassification(
            case_id=evidence.case_id,
            classification="no_conflict",
            advisory_level="PASS",
            exemption_status="not_needed",
            recommendation="continue_generation",
            requires_writer_approval=False,
            confidence=0.99,
        )
    if _has_valid_mystery_exemption(evidence):
        return ContradictionClassification(
            case_id=evidence.case_id,
            classification="intentional_mystery",
            advisory_level="ALLOW_WITH_LOCK",
            exemption_status="exempted_by_reveal_lock",
            recommendation="preserve_mystery_and_attach_reveal_lock",
            requires_writer_approval=False,
            confidence=0.93,
        )
    if evidence.pov_boundary:
        return ContradictionClassification(
            case_id=evidence.case_id,
            classification="character_misunderstanding",
            advisory_level="ALLOW_WITH_POV_TAG",
            exemption_status="exempted_by_pov_boundary",
            recommendation="tag_character_knowledge_boundary",
            requires_writer_approval=False,
            confidence=0.91,
        )
    if evidence.scheduled_reveal_episode and evidence.payoff_budget_reserved:
        return ContradictionClassification(
            case_id=evidence.case_id,
            classification="reveal_delay",
            advisory_level="ALLOW_WITH_REVEAL_BUDGET",
            exemption_status="exempted_by_reveal_schedule",
            recommendation="track_in_episode_reveal_budget",
            requires_writer_approval=False,
            confidence=0.90,
        )
    if evidence.same_canon_scope and evidence.truth_confidence_a >= 0.80 and evidence.truth_confidence_b >= 0.80:
        return ContradictionClassification(
            case_id=evidence.case_id,
            classification="true_contradiction",
            advisory_level="REVIEW_REQUIRED",
            exemption_status="not_exempted",
            recommendation="route_to_writer_review_queue",
            requires_writer_approval=True,
            confidence=0.95,
        )
    return ContradictionClassification(
        case_id=evidence.case_id,
        classification="ambiguous_conflict",
        advisory_level="REVIEW_REQUIRED",
        exemption_status="not_exempted",
        recommendation="route_to_writer_review_queue",
        requires_writer_approval=True,
        confidence=0.72,
    )


def run_stage132_classifier_matrix() -> dict[str, Any]:
    evidence = build_stage132_fixture_evidence()
    classifications = [classify_contradiction(item) for item in evidence]
    issues: list[str] = []
    if not any(result.classification == "true_contradiction" and result.requires_writer_approval for result in classifications):
        issues.append("true_contradiction_writer_review_missing")
    if any(result.hard_block_allowed for result in classifications):
        issues.append("hard_block_enabled")
    if any(result.canon_auto_resolution_allowed for result in classifications):
        issues.append("canon_auto_resolution_enabled")
    if any(result.auto_repair_allowed for result in classifications):
        issues.append("auto_repair_enabled")
    expected = {
        "true_contradiction",
        "intentional_mystery",
        "character_misunderstanding",
        "reveal_delay",
        "no_conflict",
    }
    seen = {result.classification for result in classifications}
    missing = sorted(expected - seen)
    if missing:
        issues.append(f"missing_classifications:{','.join(missing)}")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "evidence": [item.to_dict() for item in evidence],
        "classifications": [result.to_dict() for result in classifications],
        "case_count": len(classifications),
        "exemption_count": sum(1 for result in classifications if result.exemption_status.startswith("exempted")),
        "writer_review_required_count": sum(1 for result in classifications if result.requires_writer_approval),
        "hard_block_count": sum(1 for result in classifications if result.hard_block_allowed),
        "canon_auto_resolution_count": sum(1 for result in classifications if result.canon_auto_resolution_allowed),
        "auto_repair_mutation_count": sum(1 for result in classifications if result.auto_repair_allowed),
    }


def _has_valid_mystery_exemption(evidence: ContradictionEvidence) -> bool:
    return (
        bool(evidence.reveal_lock_id)
        and evidence.payoff_budget_reserved
        and evidence.writer_intent_tag == "intentional_mystery"
    )
