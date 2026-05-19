from __future__ import annotations

import json

from v1700.learning_quality_gate import run_stage135_learning_quality_gate


if __name__ == "__main__":
    print(json.dumps(run_stage135_learning_quality_gate(), ensure_ascii=False, indent=2))
