from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.dependency_conflict_preflight import run_stage158_dependency_conflict_preflight


def main() -> int:
    result = run_stage158_dependency_conflict_preflight()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
