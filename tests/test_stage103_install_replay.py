from pathlib import Path

from v1700.stage103.install_replay import run_install_replay_probe
from v1700.stage103.orchestrator import run_stage103_1_install_replay


def test_stage103_install_replay_contract_is_fresh_clone_ready():
    root = Path(__file__).resolve().parents[1]
    result = run_install_replay_probe(root)
    assert result["status"] == "pass"
    assert result["fresh_clone_ready"] is True
    assert "python tools/run_stage103_release_gate.py" in result["documented_commands"]


def test_stage103_install_replay_writes_evidence():
    root = Path(__file__).resolve().parents[1]
    result = run_stage103_1_install_replay(root)
    assert result["status"] == "pass"
    assert (root / "release/current/stage103_install_replay_report.json").exists()
    assert result["ci_replay"]["live_provider_call_count_in_release_gate"] == 0
