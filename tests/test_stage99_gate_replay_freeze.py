from pathlib import Path

from v1700.stage99.gate_replay import run_stage99_2_gate_replay_freeze

ROOT = Path(__file__).resolve().parents[1]


def test_stage99_2_replays_gates_and_writes_stage100_precheck():
    report = run_stage99_2_gate_replay_freeze(ROOT)
    assert report["status"] == "pass"
    assert report["release_gate_replay_status"] == "pass"
    assert report["regression_freeze_status"] == "pass"
    assert report["stage100_readiness_status"] == "pass"
    assert (ROOT / "release/current/stage100_readiness_precheck_report.json").exists()
