from pathlib import Path
from v1700.stage106.orchestrator import run_stage106_4_release_policy

def test_stage106_release_policy_blocks_provider_export():
    report = run_stage106_4_release_policy(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["provider_export_allowed"] is False
    assert report["full_text_export_default"] is False
