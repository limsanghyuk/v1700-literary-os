from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage91_release_gate import run_stage91_release_gate

if __name__ == "__main__":
    result = run_stage91_release_gate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
