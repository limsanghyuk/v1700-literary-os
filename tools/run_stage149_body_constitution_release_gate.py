from __future__ import annotations

import json
from pathlib import Path

from v1700.stage149 import run_stage149


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_stage149(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
