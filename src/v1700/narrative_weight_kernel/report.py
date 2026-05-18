from __future__ import annotations

import json
from pathlib import Path

from v1700.narrative_weight_kernel.character_board import score_character_board
from v1700.narrative_weight_kernel.contracts import (
    CharacterSeed,
    EventSeed,
    FeedbackSignal,
    NarrativeWeightVector,
    WeightKernelReport,
)
from v1700.narrative_weight_kernel.learning import learn_kernel_weights
from v1700.narrative_weight_kernel.relation_engine import score_relation_matrix


def build_reference_characters() -> tuple[CharacterSeed, ...]:
    return (
        CharacterSeed(
            character_id="protagonist",
            display_name="윤서",
            board_piece="king",
            dramatic_role="truth-seeking protagonist",
            desire="recover the missing record",
            wound="betrayed by the archive she trusted",
            secret="knows the first page is forged",
            relation_to_protagonist="self",
            agency_bias=0.88,
            knowledge_access=0.62,
            motif_refs=("burned_card", "north_window"),
        ),
        CharacterSeed(
            character_id="antagonist",
            display_name="도현",
            board_piece="shadow",
            dramatic_role="archive-controlling antagonist",
            desire="keep the branchpoint sealed",
            wound="lost status after the prior inquiry",
            secret="moved the ledger before the fire",
            relation_to_protagonist="opposes protagonist",
            agency_bias=0.84,
            knowledge_access=0.86,
            motif_refs=("sealed_box",),
        ),
        CharacterSeed(
            character_id="witness",
            display_name="미라",
            board_piece="bishop",
            dramatic_role="silent witness",
            desire="avoid becoming evidence",
            wound="punished for telling the truth once",
            secret="heard the erased call",
            relation_to_protagonist="reluctant ally",
            agency_bias=0.55,
            knowledge_access=0.78,
            motif_refs=("north_window",),
        ),
    )


def build_reference_events() -> tuple[EventSeed, ...]:
    return (
        EventSeed(
            event_id="E01_ARCHIVE_FIRE",
            summary="The archive burns while the protagonist discovers the forged first page.",
            episode_index=1,
            function="inciting incident",
            involved_characters=("protagonist", "antagonist"),
            causal_importance=0.92,
            reveal_refs=("burned_card", "sealed_box"),
            pressure=0.86,
        ),
        EventSeed(
            event_id="E04_WITNESS_SILENCE",
            summary="The witness refuses to answer, but her silence redirects the investigation.",
            episode_index=4,
            function="mid-arc pressure turn",
            involved_characters=("protagonist", "witness"),
            causal_importance=0.72,
            reveal_refs=("north_window",),
            pressure=0.68,
        ),
    )


def run_narrative_weight_kernel_smoke() -> dict:
    baseline = NarrativeWeightVector()
    characters = build_reference_characters()
    events = build_reference_events()
    relation_map = {
        ("protagonist", "E01_ARCHIVE_FIRE"): "antagonist",
        ("antagonist", "E01_ARCHIVE_FIRE"): "secret_keeper",
        ("witness", "E04_WITNESS_SILENCE"): "witness",
        ("protagonist", "E04_WITNESS_SILENCE"): "ally",
    }
    character_scores = score_character_board(characters, baseline)
    relation_scores = score_relation_matrix(characters, events, relation_map, baseline)
    feedback = (
        FeedbackSignal(metric="agency", observed=0.58, target=0.70, confidence=0.9, source="agency_conservation_gate"),
        FeedbackSignal(metric="relation_tension", observed=0.46, target=0.62, confidence=0.8, source="drse_relation_gate"),
        FeedbackSignal(metric="reader_attention", observed=0.52, target=0.64, confidence=0.7, source="attention_economy_gate"),
        FeedbackSignal(metric="safety_boundary", observed=1.0, target=1.0, confidence=1.0, source="node2_boundary_gate"),
    )
    learning_report = learn_kernel_weights(baseline, feedback)
    issues: list[str] = []
    if not character_scores:
        issues.append("character_scores_missing")
    if not relation_scores:
        issues.append("relation_scores_missing")
    if learning_report.status != "pass":
        issues.append("learning_report_blocked")
    if any(score.weighted_score <= 0.0 for score in character_scores + relation_scores):
        issues.append("non_positive_weighted_score")
    report = WeightKernelReport(
        stage="111.1",
        status="pass" if not issues else "blocked",
        character_scores=character_scores,
        relation_scores=relation_scores,
        learning_report=learning_report,
        invariants={
            "kernel_type": "auditable_symbolic_weight_kernel",
            "neural_network_training": False,
            "provider_call_count": 0,
            "node2_raw_reveal_access": 0,
            "character_event_relation_matrix": True,
            "bounded_self_calibration": True,
        },
        issues=tuple(issues),
    )
    return report.to_dict()


def write_narrative_weight_kernel_report(path: str | Path = "release/current/narrative_weight_kernel_pack/weight_kernel_report.json") -> dict:
    report = run_narrative_weight_kernel_smoke()
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = _markdown_summary(report)
    target.with_name("weight_kernel_summary.md").write_text(summary, encoding="utf-8")
    return report


def _markdown_summary(report: dict) -> str:
    lines = [
        "# Narrative Weight Kernel Summary",
        "",
        f"- stage: {report['stage']}",
        f"- status: {report['status']}",
        f"- character_scores: {len(report['character_scores'])}",
        f"- relation_scores: {len(report['relation_scores'])}",
        f"- bounded_self_calibration: {report['invariants']['bounded_self_calibration']}",
        f"- provider_call_count: {report['invariants']['provider_call_count']}",
        f"- node2_raw_reveal_access: {report['invariants']['node2_raw_reveal_access']}",
        "",
        "## Top character weights",
    ]
    for score in sorted(report["character_scores"], key=lambda item: item["weighted_score"], reverse=True):
        lines.append(f"- {score['character_id']}: {score['weighted_score']} ({score['board_piece']})")
    lines.extend(["", "## Learning updates"])
    for update in report["learning_report"]["update_log"]:
        lines.append(f"- {update['weight']}: {update['applied_delta']}")
    return "\n".join(lines) + "\n"
