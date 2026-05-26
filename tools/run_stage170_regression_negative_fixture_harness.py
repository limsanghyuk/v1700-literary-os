from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.evaluation_regression import run_stage170_regression_negative_fixture_harness

if __name__ == "__main__":
    result = run_stage170_regression_negative_fixture_harness(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
