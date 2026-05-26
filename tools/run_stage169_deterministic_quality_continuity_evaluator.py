from __future__ import annotations

import json
from pathlib import Path

from v1700.evaluation_engine import run_stage169_deterministic_evaluator


if __name__ == "__main__":
    print(json.dumps(run_stage169_deterministic_evaluator(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
