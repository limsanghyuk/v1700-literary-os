from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from v1700.sidecars.gitnexus.contracts import GitNexusIndexStatus


def detect_stale_gitnexus_index(repo_root: Path, status: GitNexusIndexStatus) -> GitNexusIndexStatus:
    if not status.registered:
        return GitNexusIndexStatus(
            alias=status.alias,
            registered=False,
            registry_path=status.registry_path,
            stale=True,
            reason=status.reason or "index_not_registered",
        )
    if not status.indexed_at:
        return _replace_status(status, stale=True, reason="indexed_at_missing")

    try:
        indexed_at = datetime.fromisoformat(status.indexed_at.replace("Z", "+00:00"))
    except ValueError:
        return _replace_status(status, stale=True, reason="indexed_at_unparseable")

    newest_source_mtime = _newest_source_mtime(repo_root)
    if newest_source_mtime and newest_source_mtime > indexed_at:
        return _replace_status(status, stale=True, reason="source_newer_than_index")
    return _replace_status(status, stale=False, reason="index_current_or_no_newer_source")


def _newest_source_mtime(root: Path) -> datetime | None:
    newest: float | None = None
    for path in root.rglob("*"):
        if not path.is_file() or _is_ignored(path):
            continue
        if path.suffix.lower() not in {".py", ".json", ".md", ".toml"}:
            continue
        newest = max(newest or 0.0, path.stat().st_mtime)
    if newest is None:
        return None
    return datetime.fromtimestamp(newest, tz=timezone.utc)


def _is_ignored(path: Path) -> bool:
    ignored_parts = {".git", ".gitnexus", "__pycache__", ".pytest_cache", "release"}
    return any(part in ignored_parts for part in path.parts)


def _replace_status(status: GitNexusIndexStatus, *, stale: bool, reason: str) -> GitNexusIndexStatus:
    return GitNexusIndexStatus(
        alias=status.alias,
        registered=status.registered,
        path=status.path,
        storage_path=status.storage_path,
        indexed_at=status.indexed_at,
        stats=status.stats,
        registry_path=status.registry_path,
        stale=stale,
        reason=reason,
    )
