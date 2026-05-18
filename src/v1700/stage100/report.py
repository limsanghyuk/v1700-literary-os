from __future__ import annotations

from pathlib import Path

from v1700.studio_workflow.report import write_json, write_summary

__all__ = ["write_json", "write_summary", "stage100_pack"]


def stage100_pack(root: Path, name: str) -> Path:
    path = root / "release" / "current" / name
    path.mkdir(parents=True, exist_ok=True)
    return path

