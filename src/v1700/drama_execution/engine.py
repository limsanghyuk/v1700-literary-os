from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BranchState:
    branch_id: str
    committed: bool
    rolled_back: bool
    reconverged_to: str | None

    def to_dict(self) -> dict:
        return self.__dict__.copy()

class TemporalContinuityChecker:
    def check(self, timeline: tuple[str, ...]) -> dict:
        issues = []
        if len(timeline) != len(tuple(dict.fromkeys(timeline))):
            issues.append("duplicate_timeline_position")
        if not timeline or not timeline[0].startswith("EP01") or not timeline[-1].startswith("EP03"):
            issues.append("timeline_order_not_three_episode")
        return {"status": "pass" if not issues else "blocked", "timeline": list(timeline), "issues": issues}

class EmotionalPressureValve:
    def evaluate(self, pressures: tuple[float, ...]) -> dict:
        peak = max(pressures)
        release = pressures[-1] < peak and pressures[-1] >= 0.35
        issues = []
        if peak < 0.75:
            issues.append("pressure_peak_too_low")
        if not release:
            issues.append("pressure_release_missing")
        return {"status": "pass" if not issues else "blocked", "pressures": list(pressures), "peak": peak, "controlled_release": release, "issues": issues}

class BranchCommitRollbackEngine:
    def run(self) -> dict:
        states = (
            BranchState("B1_false_accusation", True, True, "main_truth_cost"),
            BranchState("B2_withheld_letter", True, False, "main_truth_cost"),
        )
        issues = []
        if not any(s.rolled_back for s in states):
            issues.append("rollback_not_exercised")
        if not all(s.reconverged_to for s in states):
            issues.append("reconvergence_missing")
        return {"status": "pass" if not issues else "blocked", "branches": [s.to_dict() for s in states], "issues": issues}

class DramaExecutionEngine:
    def run(self) -> dict:
        temporal = TemporalContinuityChecker().check(("EP01_NIGHT", "EP02_DAWN", "EP03_NIGHT"))
        pressure = EmotionalPressureValve().evaluate((0.42, 0.68, 0.91, 0.54))
        branching = BranchCommitRollbackEngine().run()
        issues = []
        for name, report in (("temporal", temporal), ("pressure", pressure), ("branching", branching)):
            if report["status"] != "pass":
                issues.append(f"{name}_blocked")
        return {"stage": "78", "status": "pass" if not issues else "blocked", "issues": issues, "temporal_continuity": temporal, "emotional_pressure_valve": pressure, "branch_commit_rollback": branching, "provider_default_calls": 0}

def run_drama_execution_smoke() -> dict:
    return DramaExecutionEngine().run()
