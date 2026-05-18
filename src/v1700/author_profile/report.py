from __future__ import annotations
import json
from pathlib import Path


def stage106_pack(root: Path) -> Path:
    path = root / "release" / "current" / "stage106_style_genome_pack"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_summary(path: Path, title: str, bullets: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""] + [f"- {b}" for b in bullets] + [""]
    path.write_text("\n".join(lines), encoding="utf-8")
