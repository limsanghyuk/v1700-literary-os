from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_provider_runtime_report(root: Path, report: dict[str, Any]) -> Path:
    out = root / "release" / "current" / "stage97_2_provider_runtime_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out
