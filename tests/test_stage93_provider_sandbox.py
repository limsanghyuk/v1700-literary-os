from __future__ import annotations

from v1700.gates.stage93_release_gate import run_stage93_release_gate
from v1700.provider_adapters.credential_audit import audit_provider_credentials
from v1700.provider_adapters.live_sandbox import run_stage93_live_provider_sandbox
from v1700.provider_adapters.normalization import normalize_provider_response, run_stage93_response_normalization_probe


def test_stage93_credential_audit_redacts_secret_values(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-" + "test-secret-value-that-must-not-leak")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-test-secret-value-that-must-not-leak")
    monkeypatch.setenv("GOOGLE_API_KEY", "AI" + "za-test-secret-value-that-must-not-leak")
    report = audit_provider_credentials().to_dict()
    serialized = str(report)
    assert report["status"] == "pass"
    assert report["plain_secret_preview_count"] == 0
    assert ("sk-" + "test-secret-value") not in serialized
    assert "anthropic-test-secret-value" not in serialized
    assert ("AI" + "za-test-secret-value") not in serialized
    assert all("redacted_fingerprint" in item for item in report["credential_statuses"])


def test_stage93_normalizes_four_provider_shapes():
    shapes = {
        "ollama": {"message": {"content": "ollama ok"}, "done": True},
        "gpt": {"output_text": "gpt ok", "usage": {"input_tokens": 1, "output_tokens": 2}},
        "claude": {"content": [{"type": "text", "text": "claude ok"}], "stop_reason": "end_turn"},
        "gemini": {"candidates": [{"content": {"parts": [{"text": "gemini ok"}]}, "finishReason": "STOP"}]},
    }
    for kind, raw in shapes.items():
        result = normalize_provider_response(provider_id=f"{kind}_id", provider_kind=kind, request_id="r1", raw=raw)
        assert result.normalized_status == "pass"
        assert kind in result.text
        assert result.live_call_performed is False


def test_stage93_response_normalization_probe_passes():
    report = run_stage93_response_normalization_probe().to_dict()
    assert report["status"] == "pass"
    assert report["normalized_provider_count"] == 4
    assert report["live_call_count"] == 0
    assert report["provider_default_calls"] == 0


def test_stage93_live_provider_sandbox_is_release_safe():
    report = run_stage93_live_provider_sandbox(execution_allowed=False).to_dict()
    assert report["status"] == "pass"
    assert report["configured_provider_count"] == 4
    assert report["mode"] == "dry_run_release_safe"
    assert report["live_call_count"] == 0
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0


def test_stage93_release_gate_passes():
    result = run_stage93_release_gate()
    assert result["status"] == "pass"
    assert result["live_call_count"] == 0
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
