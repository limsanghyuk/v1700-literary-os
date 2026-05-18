from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.governor.contracts import GateInput, GovernorDecision, Stage125Contract


class GateGovernor:
    """Deterministic Gate25/28/29 release governor.

    Gate25 remains the primary authority. Gate28 and Gate29 are secondary gates:
    a passing Gate28 quality report and a matched Gate29 predictive negative case
    are required for the Stage125 governor to pass, but neither secondary gate can
    replace Gate25 or trigger live provider/model behavior.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.contract = Stage125Contract()

    def evaluate(self) -> GovernorDecision:
        gate25_report = self._read_json("release/current/stage120_gate25_nie_v1_report.json")
        gate28_report = self._read_json("release/current/stage123_gate28_report.json")
        gate29_report = self._read_json("release/current/stage124_gate29_report.json")
        stage123 = self._read_json("release/current/stage123_asd_gate28_absorption_report.json")
        stage124 = self._read_json("release/current/stage124_pne_gate29_absorption_report.json")

        gates = (
            GateInput(
                gate_id="Gate25",
                stage=str(gate25_report.get("stage", "120")),
                mode="primary",
                status=str(gate25_report.get("status", "missing")),
                report_path="release/current/stage120_gate25_nie_v1_report.json",
                issues=tuple(gate25_report.get("issues", []) or []),
                metrics={
                    "component_count": len(gate25_report.get("component_matrix", {}) or {}),
                    "provider_default_calls": gate25_report.get("provider_default_calls", 0),
                    "node2_raw_reveal_access": gate25_report.get("node2_raw_reveal_access", 0),
                },
            ),
            GateInput(
                gate_id="Gate28",
                stage=str(stage123.get("stage", "123")),
                mode="secondary_quality",
                status=str(gate28_report.get("status", "missing")),
                report_path="release/current/stage123_gate28_report.json",
                issues=tuple(gate28_report.get("issues", []) or []),
                metrics={
                    "combined_quality": gate28_report.get("combined_quality"),
                    "authority_mode": gate28_report.get("authority_mode"),
                    "mutation_count": stage123.get("auto_repair_mutation_count", 0),
                },
            ),
            GateInput(
                gate_id="Gate29",
                stage=str(stage124.get("stage", "124")),
                mode="secondary_predictive",
                status="pass" if self._gate29_expected_behavior(gate29_report) else "blocked",
                report_path="release/current/stage124_gate29_report.json",
                issues=tuple(gate29_report.get("issues", []) or []),
                metrics={
                    "low_risk_status": (gate29_report.get("low_risk_case", {}) or {}).get("status"),
                    "high_risk_status": (gate29_report.get("high_risk_case", {}) or {}).get("status"),
                    "feedback_precision": self._extract_feedback_precision(gate29_report),
                    "runtime_training_count": stage124.get("pne_runtime_training_count", 0),
                },
            ),
        )

        invariants = self._invariants(gate25_report, stage123, stage124)
        checks = {
            "gate25_primary_pass": gates[0].status == "pass" and gates[0].mode == "primary",
            "gate28_secondary_quality_pass": gates[1].status == "pass" and gates[1].metrics.get("authority_mode") == "secondary_quality_gate",
            "gate29_secondary_predictive_expected_behavior": gates[2].status == "pass",
            "gate28_not_primary": invariants["gate28_primary_authority_enabled"] is False,
            "gate29_not_primary": invariants["gate29_primary_authority_enabled"] is False,
            "no_release_runtime_training": invariants["release_gate_runtime_training_enabled"] is False and invariants["pne_runtime_training_count"] == 0,
            "no_auto_repair_mutation": invariants["auto_repair_mutation_count"] == 0,
            "provider_zero": invariants["provider_default_calls"] == 0 and invariants["live_provider_call_count_in_release_gate"] == 0,
            "node2_boundary": invariants["node2_raw_reveal_access"] == 0,
            "raw_manuscript_leakage_zero": invariants["raw_manuscript_provider_leakage"] == 0,
            "credential_leakage_zero": invariants["credential_leakage"] == 0,
        }
        blocked_by = tuple(name for name, ok in checks.items() if not ok)
        warnings: tuple[str, ...] = ()
        status = "pass" if not blocked_by else "blocked"
        return GovernorDecision(
            status=status,
            authority_mode="Gate25_primary_with_Gate28_Gate29_secondary_governor",
            primary_gate="Gate25",
            secondary_gates=("Gate28", "Gate29"),
            blocked_by=blocked_by,
            warnings=warnings,
            checks=checks,
            gate_inputs=gates,
            invariants=invariants,
        )

    def _read_json(self, rel: str) -> dict[str, Any]:
        path = self.root / rel
        if not path.exists():
            return {"status": "missing", "issues": [f"missing:{rel}"]}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "blocked", "issues": [f"invalid_json:{rel}:{exc}"]}

    @staticmethod
    def _gate29_expected_behavior(report: dict[str, Any]) -> bool:
        low = report.get("low_risk_case", {}) or {}
        high = report.get("high_risk_case", {}) or {}
        return low.get("status") == "pass" and high.get("status") == "blocked"

    @staticmethod
    def _extract_feedback_precision(report: dict[str, Any]) -> float:
        low = report.get("low_risk_case", {}) or {}
        feedback = low.get("feedback_report", {}) or {}
        metrics = feedback.get("metrics", {}) or {}
        try:
            return float(metrics.get("precision", 0.0))
        except Exception:
            return 0.0

    @staticmethod
    def _invariants(gate25: dict[str, Any], stage123: dict[str, Any], stage124: dict[str, Any]) -> dict[str, Any]:
        return {
            "provider_default_calls": int(gate25.get("provider_default_calls", 0) or 0)
            + int(stage123.get("provider_default_calls", 0) or 0)
            + int(stage124.get("provider_default_calls", 0) or 0),
            "live_provider_call_count_in_release_gate": int(gate25.get("live_provider_call_count_in_release_gate", 0) or 0)
            + int(stage123.get("live_provider_call_count_in_release_gate", 0) or 0)
            + int(stage124.get("live_provider_call_count_in_release_gate", 0) or 0),
            "gate28_primary_authority_enabled": bool((stage123.get("absorption_policy", {}) or {}).get("gate28_primary_authority_enabled", False)),
            "gate29_primary_authority_enabled": bool((stage124.get("absorption_policy", {}) or {}).get("gate29_primary_authority_enabled", False)),
            "release_gate_runtime_training_enabled": bool((stage124.get("absorption_policy", {}) or {}).get("release_gate_runtime_training_enabled", False)),
            "pne_runtime_training_count": int(stage124.get("pne_runtime_training_count", 0) or 0),
            "auto_repair_mutation_count": int(stage123.get("auto_repair_mutation_count", 0) or 0),
            "node2_raw_reveal_access": int(gate25.get("node2_raw_reveal_access", 0) or 0)
            + int(stage123.get("node2_raw_reveal_access", 0) or 0)
            + int(stage124.get("node2_raw_reveal_access", 0) or 0),
            "raw_manuscript_provider_leakage": int(gate25.get("raw_manuscript_provider_leakage", 0) or 0)
            + int(stage123.get("raw_manuscript_provider_leakage", 0) or 0)
            + int(stage124.get("raw_manuscript_provider_leakage", 0) or 0),
            "credential_leakage": int(gate25.get("credential_leakage", 0) or 0)
            + int(stage123.get("credential_leakage", 0) or 0)
            + int(stage124.get("credential_leakage", 0) or 0),
        }
