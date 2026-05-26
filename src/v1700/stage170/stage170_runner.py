from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.evaluation_regression import run_stage170_regression_negative_fixture_harness


def run_stage170(root: Path | None = None) -> dict[str, Any]:
    return run_stage170_regression_negative_fixture_harness(root)
