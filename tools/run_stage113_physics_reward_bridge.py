from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.stage113.orchestrator import run_stage113

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_stage113(root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
