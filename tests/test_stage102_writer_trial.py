from pathlib import Path

from v1700.stage102.orchestrator import run_stage102_1_writer_trial

ROOT = Path(__file__).resolve().parents[1]


def test_stage102_writer_trial_completes_local_workflow():
    report = run_stage102_1_writer_trial(ROOT)
    assert report["status"] == "pass"
    assert report["seed_count"] >= 3
    assert report["task_completion_count"] == report["task_count"]
    assert report["average_friction_score"] >= 8.0
    assert report["provider_default_calls"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
