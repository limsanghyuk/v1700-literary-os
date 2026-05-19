from __future__ import annotations

import json

from v1700.contradiction_classifier import run_stage132_contradiction_classifier


if __name__ == "__main__":
    print(json.dumps(run_stage132_contradiction_classifier(), ensure_ascii=False, indent=2))
