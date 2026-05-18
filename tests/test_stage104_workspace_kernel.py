from pathlib import Path
from v1700.stage104.orchestrator import run_stage104_1_workspace_kernel
ROOT = Path(__file__).resolve().parents[1]

def test_stage104_workspace_kernel_passes():
    report = run_stage104_1_workspace_kernel(ROOT)
    assert report["status"] == "pass"
    assert report["session"]["provider_call_count"] == 0
    assert report["workspace"]["workspace_state"]["raw_manuscript_provider_leakage"] == 0
