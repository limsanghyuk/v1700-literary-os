from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.evaluation_body_contract import run_stage167_evaluation_contract


if __name__ == "__main__":
    payload = run_stage167_evaluation_contract()
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    raise SystemExit(0 if payload.get("status") == "pass" else 1)

