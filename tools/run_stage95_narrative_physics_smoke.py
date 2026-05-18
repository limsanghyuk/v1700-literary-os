from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.narrative_physics.engine import run_stage95_narrative_physics_smoke


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_stage95_narrative_physics_smoke()
    out = root / "release" / "current" / "stage95_narrative_physics_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
