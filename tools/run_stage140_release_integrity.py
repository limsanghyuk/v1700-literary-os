from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.release_integrity import run_stage140_release_integrity


def main() -> int:
    result = run_stage140_release_integrity(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("status") == "pass":
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
