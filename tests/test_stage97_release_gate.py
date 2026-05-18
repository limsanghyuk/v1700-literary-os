from pathlib import Path

from v1700.gates.stage97_release_gate import run_stage97_release_gate
from v1700.longform_endurance.endurance_orchestrator import run_stage97_longform_endurance


def test_stage97_longform_endurance_required_and_extended_proofs_pass():
    report = run_stage97_longform_endurance(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["required_16_episode_proof"]["status"] == "pass"
    assert report["extended_24_episode_proof"]["status"] == "pass"
    assert report["scene_count_estimate"] >= 160


def test_stage97_release_gate_preserves_boundaries():
    report = run_stage97_release_gate(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["episode_count_verified"] == 16
    assert report["critical_debt_default_count"] == 0
    assert report["provider_call_count"] == 0
    assert report["node2_raw_reveal_access"] == 0
