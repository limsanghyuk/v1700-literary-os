from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.studio_workflow.studio_orchestrator import run_stage98_1_review_queue


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = run_stage98_1_review_queue(root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
