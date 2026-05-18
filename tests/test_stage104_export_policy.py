from pathlib import Path
from v1700.studio_beta.import_export import build_studio_beta_export
ROOT = Path(__file__).resolve().parents[1]

def test_export_policy_defaults_to_feature_only():
    export = build_studio_beta_export(ROOT)
    assert export["status"] == "pass"
    assert export["includes_full_text"] is False
    assert export["includes_feature_reports"] is True
