from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.render_plan_builder import run_stage163_deterministic_render_plan_builder

if __name__ == "__main__":
    payload = run_stage163_deterministic_render_plan_builder()
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    raise SystemExit(0 if payload["status"] == "pass" else 1)
