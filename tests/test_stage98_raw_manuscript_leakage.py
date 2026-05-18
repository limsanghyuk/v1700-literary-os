from pathlib import Path

from v1700.gates.stage98_release_gate import run_stage98_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_release_gate_blocks_raw_manuscript_and_provider_leakage():
    gate = run_stage98_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["raw_manuscript_provider_leakage"] == 0
    assert gate["full_text_exported"] is False
    assert gate["provider_call_count"] == 0
    assert gate["node2_raw_reveal_access"] == 0
