from pathlib import Path
from v1700.stage107_5.provider_sandbox_orchestrator import run_stage107_5_0_sandbox_preflight

def test_stage107_5_sandbox_preflight_passes():
    result = run_stage107_5_0_sandbox_preflight(Path.cwd())
    assert result['status'] == 'pass'
    assert result['checks']['release_gate_isolation_pass'] is True
