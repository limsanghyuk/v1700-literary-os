from pathlib import Path

from v1700.studio_workflow.studio_orchestrator import (
    run_stage98_0_studio_workflow_core,
    run_stage98_1_review_queue,
    run_stage98_2_publishing_package,
    run_stage98_studio_workflow,
)

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_0_runs_before_review_and_publishing_reports():
    report = run_stage98_0_studio_workflow_core(ROOT)
    assert report["stage"] == "98.0"
    assert report["status"] == "pass"
    assert report["episode_board_status"] == "pass"
    assert (ROOT / "release/current/stage98_0_studio_workflow_core_report.json").exists()


def test_stage98_1_declares_stage98_0_baseline():
    report = run_stage98_1_review_queue(ROOT)
    assert report["stage"] == "98.1"
    assert report["baseline_stage"] == "98.0"
    assert report["stage98_0_status"] == "pass"
    assert report["writer_approval_guard_status"] == "pass"
    assert (ROOT / "release/current/stage98_1_review_queue_report.json").exists()


def test_stage98_2_declares_stage98_1_baseline_and_feature_only_package():
    report = run_stage98_2_publishing_package(ROOT)
    assert report["stage"] == "98.2"
    assert report["baseline_stage"] == "98.1"
    assert report["stage98_1_status"] == "pass"
    assert report["full_text_exported"] is False
    assert (ROOT / "release/current/stage98_2_publishing_package_report.json").exists()


def test_stage98_final_workflow_records_ordered_stage_sequence():
    report = run_stage98_studio_workflow(ROOT)
    assert report["stage_sequence"] == ["98.0", "98.1", "98.2"]
    assert report["stage98_0_status"] == "pass"
    assert report["stage98_1_status"] == "pass"
    assert report["stage98_2_status"] == "pass"
