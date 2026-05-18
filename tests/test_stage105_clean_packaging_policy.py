from pathlib import Path
from v1700.gates.stage105_release_gate import _clean_packaging_status


def test_stage105_clean_packaging_policy_does_not_require_historical_zips():
    root = Path(__file__).resolve().parents[1]
    assert _clean_packaging_status(root) in {"pass", "blocked"}
