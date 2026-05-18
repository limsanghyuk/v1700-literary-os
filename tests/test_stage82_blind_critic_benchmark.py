from v1700.blind_critic import BlindCriticEvaluationHarness, run_blind_critic_benchmark
from v1700.gates.stage82_release_gate import run_stage82_release_gate


def test_blind_critic_benchmark_has_three_blinded_candidates_and_v1700_wins():
    report = BlindCriticEvaluationHarness().run()
    assert report.status == "pass"
    assert len(report.blind_candidates) == 3
    assert {candidate.hidden_label for candidate in report.blind_candidates} == {"A", "B", "C"}
    assert report.winner_source_label == BlindCriticEvaluationHarness.V1700
    assert report.v1700_margin_over_pure_gpt >= 1.0


def test_blind_critic_axes_include_korean_drama_composition_layers():
    result = run_blind_critic_benchmark()
    axes = set(result["axes"])
    assert "series_story_arc" in axes
    assert "macro_plot_architecture" in axes
    assert "episode_microplot_linkage" in axes
    assert "supporting_character_web" in axes
    assert result["reveal_leakage_count"] == 0
    assert result["provider_default_calls"] == 0


def test_stage82_release_gate_passes_and_depends_on_stage81_1():
    result = run_stage82_release_gate()
    assert result["status"] == "pass"
    assert result["stage81_1_release_gate"]["status"] == "pass"
    assert result["blind_critic_benchmark"]["status"] == "pass"
    assert result["winner_source_label"] == BlindCriticEvaluationHarness.V1700
    assert result["node2_raw_reveal_access_count"] == 0
