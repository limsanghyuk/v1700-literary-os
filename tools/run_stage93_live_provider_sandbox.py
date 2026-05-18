from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.provider_adapters.live_sandbox import run_stage93_live_provider_sandbox

if __name__ == "__main__":
    result = run_stage93_live_provider_sandbox().to_dict()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
