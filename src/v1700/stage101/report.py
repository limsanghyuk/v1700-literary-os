from __future__ import annotations

from pathlib import Path

from v1700.stage100.report import write_json, write_summary

__all__ = ["stage101_pack", "write_json", "write_summary"]


def stage101_pack(root: Path, name: str) -> Path:
    path = root / "release" / "current" / name
    path.mkdir(parents=True, exist_ok=True)
    return path

