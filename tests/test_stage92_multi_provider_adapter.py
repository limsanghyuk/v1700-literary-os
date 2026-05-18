from __future__ import annotations

from v1700.gates.stage92_release_gate import run_stage92_release_gate
from v1700.provider_adapters.config import build_default_multi_provider_configs
from v1700.provider_adapters.router import MultiProviderAdapterRouter, run_stage92_multi_adapter_smoke
from v1700.provider_adapters.studio_bridge import build_stage92_studio_workspace


def test_stage92_configures_four_required_providers_without_live_calls():
    configs = build_default_multi_provider_configs(allow_live_call=False)
    assert {config.provider_kind for config in configs} == {"ollama", "gpt", "claude", "gemini"}
    assert len(configs) == 4
    assert all(config.allow_live_call is False for config in configs)


def test_stage92_router_dry_run_all_providers():
    report = run_stage92_multi_adapter_smoke()
    assert report["status"] == "pass"
    assert report["configured_provider_count"] == 4
    assert report["enabled_provider_count"] == 4
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0
    assert report["live_call_count"] == 0
    assert {item["provider_kind"] for item in report["health_checks"]} == {"ollama", "gpt", "claude", "gemini"}
    assert all(item["live_call_performed"] is False for item in report["dry_run_responses"])


def test_stage92_studio_workspace_contains_provider_panel():
    workspace = build_stage92_studio_workspace()
    panel = workspace.panel("multi_provider_adapter_panel")
    assert workspace.stage == "92"
    assert panel.item_count == 4
    assert workspace.provider_default_calls == 0
    assert workspace.node2_raw_reveal_access_count == 0


def test_stage92_release_gate_passes():
    result = run_stage92_release_gate()
    assert result["status"] == "pass"
    assert result["checks"]["stage92_multi_adapter_smoke"]["configured_provider_count"] == 4
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
