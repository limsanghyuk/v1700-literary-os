from __future__ import annotations

import json
from pathlib import Path

from v1700.gates.stage149_release_gate import run_stage149_release_gate


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_stage149_release_gate(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
