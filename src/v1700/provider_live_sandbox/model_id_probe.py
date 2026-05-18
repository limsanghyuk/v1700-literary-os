from __future__ import annotations
from .contracts import ModelIdProbeResult, ProviderSandboxConfig
from .credential_loader import credential_status

def probe_model_ids(config: ProviderSandboxConfig) -> list[dict]:
    results: list[dict] = []
    for provider_id in config.provider_ids:
        alias = config.model_aliases.get(provider_id, f'env:{provider_id.upper()}_MODEL_ID')
        cred = credential_status(provider_id)
        if provider_id == 'ollama':
            status = 'PASS' if alias else 'WARN'
            reason = 'ollama_model_alias_configured' if alias else 'ollama_model_missing'
        elif config.sandbox_enabled and config.allow_live_provider_calls and cred.get('present'):
            # We intentionally avoid broad model-list calls here. A live generation probe is run separately.
            status = 'PASS'
            reason = 'credential_present_model_alias_ready_for_live_probe'
        else:
            status = 'SKIPPED'
            reason = 'live_probe_not_enabled_or_credential_missing'
        results.append(ModelIdProbeResult(provider_id, alias, alias if status in {'PASS','WARN'} else None, status, reason, False).to_dict())
    return results
