from v1700.provider_live_sandbox.sandbox_config import ProviderSandboxConfig
from v1700.provider_live_sandbox.live_call_guard import release_path_isolated, sandbox_live_calls_allowed

def test_release_isolation_blocks_release_gate_affected():
    cfg = ProviderSandboxConfig(release_gate_affected=True)
    assert release_path_isolated(cfg)['status'] == 'blocked'

def test_live_calls_require_explicit_opt_in():
    cfg = ProviderSandboxConfig()
    allowed, issues = sandbox_live_calls_allowed(cfg)
    assert allowed is False
    assert 'sandbox_not_enabled' in issues
