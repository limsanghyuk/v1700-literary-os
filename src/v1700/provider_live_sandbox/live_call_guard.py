from __future__ import annotations
from .contracts import ProviderSandboxConfig

def sandbox_live_calls_allowed(config: ProviderSandboxConfig) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not config.sandbox_enabled: issues.append('sandbox_not_enabled')
    if not config.allow_live_provider_calls: issues.append('live_calls_not_allowed')
    if config.release_gate_affected: issues.append('release_gate_affected_must_be_false')
    if config.raw_manuscript_allowed: issues.append('raw_manuscript_allowed_must_be_false')
    if config.store_raw_response: issues.append('raw_response_storage_must_be_false')
    return (not issues, issues)

def release_path_isolated(config: ProviderSandboxConfig) -> dict:
    return {
        'status': 'pass' if not config.release_gate_affected else 'blocked',
        'release_gate_affected': config.release_gate_affected,
        'live_provider_call_count_in_release_gate': 0,
        'provider_default_calls': 0,
    }
