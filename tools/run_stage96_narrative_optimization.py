from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.narrative_optimization.optimizer import run_narrative_physics_optimization


if __name__ == "__main__":
    result = run_narrative_physics_optimization()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
