from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage72_2_release_gate import run_stage72_2_release_gate


ROOT = Path(__file__).resolve().parents[1]


def test_stage72_2_release_gate_passes_and_preserves_safety_invariants():
    report = run_stage72_2_release_gate(ROOT)

    assert report["stage"] == "72.2"
    assert report["status"] == "pass"
    assert report["gitnexus_optional_only"] is True
    assert report["python_fallback_available"] is True
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0
    assert report["checks"]["shape_check"]["status"] == "pass"


def test_main_release_gate_includes_stage72_2_when_active():
    report = run_release_gate()

    assert report["status"] == "pass"
    assert report["stage72_2_release_gate"]["status"] == "pass"
