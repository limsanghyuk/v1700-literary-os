from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.stage99.impact_baseline import run_stage99_0_gitnexus_impact_baseline


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = run_stage99_0_gitnexus_impact_baseline(root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
