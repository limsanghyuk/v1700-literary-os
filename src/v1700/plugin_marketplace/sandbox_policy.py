from __future__ import annotations
from .contracts import PluginManifest

def sandbox_policy_matrix(plugins: list[PluginManifest]) -> dict:
    rows=[]
    blockers=[]
    for p in plugins:
        row = {
            "plugin_id": p.plugin_id,
            "network_default": "blocked",
            "filesystem_write_scope": "release/current/stage109_plugin_pack only" if p.writes_release_evidence else "none",
            "raw_manuscript_access": False,
            "credential_access": False,
            "live_provider_default": False,
            "manual_review_required": p.trust_level != "core" or p.requires_live_provider,
        }
        if p.requires_raw_manuscript:
            blockers.append(f"raw_manuscript_access:{p.plugin_id}")
        if p.enabled_by_default:
            blockers.append(f"enabled_by_default:{p.plugin_id}")
        rows.append(row)
    return {"status":"pass" if not blockers else "blocked", "rows":rows, "blockers":blockers}
