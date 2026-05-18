from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.provider_ensemble.arbiter import run_provider_ensemble_arbitration


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_provider_ensemble_arbitration(root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
