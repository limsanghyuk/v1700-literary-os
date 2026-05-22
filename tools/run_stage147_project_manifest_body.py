from __future__ import annotations

import json
from pathlib import Path

from v1700.stage147 import run_stage147


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_stage147(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
