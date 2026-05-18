from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.legacy_logic_survival_gate import run_legacy_logic_survival_gate


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_legacy_logic_survival_gate(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
