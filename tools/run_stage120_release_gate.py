from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from v1700.gates.stage120_release_gate import run_stage120_release_gate

if __name__ == "__main__":
    result = run_stage120_release_gate(ROOT)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
