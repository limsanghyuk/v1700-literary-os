from pathlib import Path

from v1700.stage102.orchestrator import run_stage102_2_blind_benchmark

ROOT = Path(__file__).resolve().parents[1]


def test_stage102_blind_benchmark_scores_v1700_family_without_identity_leakage():
    report = run_stage102_2_blind_benchmark(ROOT)
    assert report["status"] == "pass"
    assert report["candidate_count"] >= 8
    assert report["reviewer_count"] >= 3
    assert report["winner_mode"] in {"V1700_PROSE", "V1700_SCENARIO", "V1700_HYBRID"}
    assert report["v1700_margin_over_pure_gpt"] >= 0.5
    assert report["blind_identity_leakage"] == 0
    assert report["provider_default_calls"] == 0
