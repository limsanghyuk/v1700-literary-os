from v1700.narrative_weight_kernel import (
    CharacterSeed,
    EventSeed,
    FeedbackSignal,
    NarrativeWeightVector,
    learn_kernel_weights,
    run_narrative_weight_kernel_smoke,
    score_character_event_relation,
    score_character_profile,
)


def test_character_board_weights_explain_multiple_axes():
    protagonist = CharacterSeed(
        character_id="hero",
        display_name="Hero",
        board_piece="king",
        dramatic_role="protagonist",
        desire="find truth",
        wound="lost trust",
        secret="knows a forbidden fact",
        agency_bias=0.9,
        knowledge_access=0.7,
        motif_refs=("key", "rain"),
    )
    score = score_character_profile(protagonist, NarrativeWeightVector())
    assert score.weighted_score > 0.7
    assert score.axis_scores["agency"] >= 0.9
    assert score.axis_scores["reveal_pressure"] > 0.7
    assert any("secret_increases_reveal_pressure" in note for note in score.explanation)


def test_character_event_relation_matrix_scores_causality_and_reveal_pressure():
    character = CharacterSeed(
        character_id="witness",
        display_name="Witness",
        board_piece="bishop",
        dramatic_role="witness",
        desire="avoid testimony",
        wound="was punished",
        secret="heard the call",
        agency_bias=0.6,
        knowledge_access=0.8,
        motif_refs=("window",),
    )
    event = EventSeed(
        event_id="E02",
        summary="Witness refuses to answer near the window.",
        episode_index=2,
        function="pressure turn",
        involved_characters=("witness",),
        causal_importance=0.85,
        reveal_refs=("window",),
        pressure=0.78,
    )
    score = score_character_event_relation(character, event, "witness")
    assert score.weighted_score > 0.6
    assert score.axis_scores["event_causality"] > 0.9
    assert "causal_anchor" in score.learning_tags
    assert "secret_event_overlap" in score.learning_tags


def test_kernel_learning_is_bounded_and_auditable():
    baseline = NarrativeWeightVector()
    report = learn_kernel_weights(
        baseline,
        (
            FeedbackSignal(metric="agency", observed=0.2, target=0.95, confidence=1.0, source="unit"),
            FeedbackSignal(metric="safety_boundary", observed=1.0, target=1.0, confidence=1.0, source="unit"),
        ),
    )
    assert report.status == "pass"
    assert round(report.learned_weights.agency - baseline.agency, 4) <= 0.08
    assert report.learned_weights.safety_boundary >= baseline.safety_boundary
    assert report.drift_guard["status"] == "pass"
    assert report.update_log


def test_weight_kernel_smoke_passes_without_provider_or_node2_access():
    report = run_narrative_weight_kernel_smoke()
    assert report["status"] == "pass"
    assert report["invariants"]["provider_call_count"] == 0
    assert report["invariants"]["node2_raw_reveal_access"] == 0
    assert report["invariants"]["character_event_relation_matrix"] is True
    assert report["learning_report"]["status"] == "pass"
