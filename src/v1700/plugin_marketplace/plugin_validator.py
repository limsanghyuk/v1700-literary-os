from __future__ import annotations
from .contracts import PluginManifest, PluginValidationResult

ALLOWED_KINDS = {"genre_pack", "evaluator_pack", "export_pack", "provider_adapter_pack", "studio_extension"}

def validate_plugin_manifest(plugin: PluginManifest) -> PluginValidationResult:
    issues: list[str] = []
    if not plugin.plugin_id or "." not in plugin.plugin_id:
        issues.append("plugin_id_not_namespaced")
    if plugin.kind not in ALLOWED_KINDS:
        issues.append("unknown_plugin_kind")
    if plugin.enabled_by_default:
        issues.append("plugin_enabled_by_default")
    if plugin.requires_raw_manuscript:
        issues.append("plugin_requires_raw_manuscript")
    if plugin.requires_live_provider and plugin.trust_level == "core":
        issues.append("core_plugin_requires_live_provider")
    if not plugin.branchpoint_trace_id.startswith("bp-stage109-"):
        issues.append("missing_stage109_branchpoint_trace")
    if not plugin.test_target.startswith("tests/test_stage109_"):
        issues.append("missing_stage109_test_target")
    return PluginValidationResult(plugin.plugin_id, "pass" if not issues else "blocked", issues)
