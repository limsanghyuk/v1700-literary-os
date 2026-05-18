from v1700.provider_live_sandbox.sandbox_config import load_sandbox_config
from v1700.provider_live_sandbox.model_id_probe import probe_model_ids

def test_model_id_probe_shape():
    results = probe_model_ids(load_sandbox_config())
    assert {r['provider_id'] for r in results} >= {'openai','anthropic','gemini','ollama'}
    assert all('probe_status' in r for r in results)
