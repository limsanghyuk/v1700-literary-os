from __future__ import annotations

import json
from pathlib import Path

from v1700.sidecars.gitnexus.contracts import GitNexusAdapterConfig, GitNexusIndexStatus


def load_gitnexus_registry(config: GitNexusAdapterConfig | None = None) -> list[dict]:
    resolved = (config or GitNexusAdapterConfig()).resolved_registry_path()
    if not resolved.exists():
        return []
    try:
        data = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def get_gitnexus_index_status(
    alias: str = "v1700_stage72_3_ascii",
    config: GitNexusAdapterConfig | None = None,
) -> GitNexusIndexStatus:
    resolved_config = config or GitNexusAdapterConfig(repo_alias=alias)
    registry_path = resolved_config.resolved_registry_path()
    for item in load_gitnexus_registry(resolved_config):
        if item.get("name") == alias:
            return GitNexusIndexStatus(
                alias=alias,
                registered=True,
                path=item.get("path", ""),
                storage_path=item.get("storagePath", ""),
                indexed_at=item.get("indexedAt", ""),
                stats=item.get("stats", {}),
                registry_path=str(registry_path),
            )
    return GitNexusIndexStatus(
        alias=alias,
        registered=False,
        registry_path=str(registry_path),
        reason="alias_not_registered",
    )


def gitnexus_index_under_workspace(status: GitNexusIndexStatus, workspace_root: Path) -> bool:
    if not status.path:
        return False
    try:
        Path(status.path).resolve().relative_to(workspace_root.resolve())
    except ValueError:
        return False
    return True
