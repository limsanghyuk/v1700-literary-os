from __future__ import annotations

from .prose_board import build_prose_board
from .scenario_board import build_scenario_board


def build_unified_board() -> dict:
    prose = build_prose_board()
    scenario = build_scenario_board()
    checks = {
        "prose_board_pass": prose.get("status") == "pass",
        "scenario_board_pass": scenario.get("status") == "pass",
        "metric_conflation_prevented": prose.get("mode") != scenario.get("mode"),
        "provider_zero": prose.get("provider_call_count", 1) == 0 and scenario.get("provider_call_count", 1) == 0,
    }
    issues = [name for name, ok in checks.items() if not ok]
    return {
        "stage": "104.2",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "prose_board": prose,
        "scenario_board": scenario,
        "active_modes": ["PROSE", "SCENARIO", "REVIEW"],
    }
