from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_summary(path: Path, title: str, bullets: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = [f"# {title}", ""] + [f"- {bullet}" for bullet in bullets]
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def stage104_pack(root: Path) -> Path:
    pack = root / "release" / "current" / "stage104_studio_beta_pack"
    pack.mkdir(parents=True, exist_ok=True)
    return pack
