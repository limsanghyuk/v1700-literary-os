from __future__ import annotations

from .project_workspace import build_sample_workspace


def build_workspace_state_report() -> dict:
    workspace = build_sample_workspace()
    state = workspace["workspace_state"]
    checks = {
        "workspace_has_scene_cards": bool(state.get("scene_cards")),
        "export_ready_without_blocks": state.get("export_ready") is True and state.get("unresolved_block_count") == 0,
        "raw_manuscript_provider_leakage_zero": state.get("raw_manuscript_provider_leakage") == 0,
        "node2_raw_reveal_access_zero": state.get("node2_raw_reveal_access") == 0,
    }
    issues = [name for name, ok in checks.items() if not ok]
    return {"status": "pass" if not issues else "blocked", "checks": checks, "issues": issues, **workspace}
