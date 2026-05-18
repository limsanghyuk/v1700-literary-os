from v1700.provider_live_sandbox.sandbox_config import load_sandbox_config
from v1700.provider_live_sandbox import openai_live_adapter, anthropic_live_adapter, gemini_live_adapter, ollama_live_adapter

def test_adapter_contracts_release_safe():
    config = load_sandbox_config()
    for adapter in (openai_live_adapter, anthropic_live_adapter, gemini_live_adapter, ollama_live_adapter):
        status = adapter.contract_status(config)
        assert status['status'] == 'pass'
        assert status['release_safe_default'] is True
