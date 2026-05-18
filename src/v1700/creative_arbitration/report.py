from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def stage105_pack(root: Path) -> Path:
    pack = root / "release" / "current" / "stage105_creative_arbitration_pack"
    pack.mkdir(parents=True, exist_ok=True)
    return pack


def write_json(path: Path, payload: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def write_summary(path: Path, title: str, lines: Iterable[str]) -> None:
    body = "# " + title + "\n\n" + "\n".join(f"- {line}" for line in lines) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
