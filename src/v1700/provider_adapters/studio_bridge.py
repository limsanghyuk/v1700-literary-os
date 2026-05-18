from __future__ import annotations

from dataclasses import replace

from v1700.provider_adapters.router import MultiProviderAdapterRouter
from v1700.writer_studio.contracts import StudioPanel, WriterStudioWorkspace
from v1700.writer_studio.persistence import build_stage91_base_workspace


def build_stage92_provider_panel() -> StudioPanel:
    report = MultiProviderAdapterRouter().smoke_report().to_dict()
    items = tuple(
        {
            "provider_id": health["provider_id"],
            "provider_kind": health["provider_kind"],
            "status": health["status"],
            "model": health["model"],
            "endpoint": health["endpoint"],
            "api_key_env": health["api_key_env"] or "none",
            "live_call_performed": health["live_call_performed"],
        }
        for health in report["health_checks"]
    )
    return StudioPanel(
        panel_id="multi_provider_adapter_panel",
        title="Multi-Provider Adapter Panel",
        purpose="Configures Ollama, GPT, Claude, and Gemini for a developer workstation while preserving provider-zero release gates.",
        source_stage="stage92",
        items=items,
        blocking_rules=(
            "must_configure_ollama_gpt_claude_gemini",
            "release_gate_must_not_perform_live_provider_calls",
            "provider_default_calls_must_remain_0",
        ),
    )


def build_stage92_studio_workspace() -> WriterStudioWorkspace:
    base = build_stage91_base_workspace()
    provider_panel = build_stage92_provider_panel()
    panels = tuple(base.panels) + (provider_panel,)
    return replace(
        base,
        stage="92",
        title="Writer Studio Runtime with Local Multi-Provider Adapter",
        panels=panels,
        inherited_stages=("stage91",) + tuple(base.inherited_stages),
        export_targets=tuple(sorted(set(base.export_targets + ("multi_provider_adapter_report",)))),
    )


def run_stage92_studio_bridge_smoke() -> dict:
    workspace = build_stage92_studio_workspace()
    provider_panel = workspace.panel("multi_provider_adapter_panel")
    issues: list[str] = []
    if workspace.stage != "92":
        issues.append("workspace_stage_not_92")
    if provider_panel.item_count != 4:
        issues.append("provider_panel_item_count_not_4")
    if workspace.provider_default_calls != 0:
        issues.append("provider_default_calls_not_zero")
    if workspace.node2_raw_reveal_access_count != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "92",
        "status": "pass" if not issues else "blocked",
        "workspace_stage": workspace.stage,
        "studio_panel_count": workspace.panel_count,
        "provider_panel_item_count": provider_panel.item_count,
        "provider_default_calls": workspace.provider_default_calls,
        "node2_raw_reveal_access_count": workspace.node2_raw_reveal_access_count,
        "issues": issues,
    }
