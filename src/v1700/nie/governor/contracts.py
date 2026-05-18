from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

GateMode = Literal["primary", "secondary_quality", "secondary_predictive", "advisory", "blocked"]
Decision = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class GateInput:
    gate_id: str
    stage: str
    mode: GateMode
    status: str
    report_path: str
    issues: tuple[str, ...] = ()
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "stage": self.stage,
            "mode": self.mode,
            "status": self.status,
            "report_path": self.report_path,
            "issues": list(self.issues),
            "metrics": self.metrics,
        }


@dataclass(frozen=True)
class GovernorDecision:
    status: Decision
    authority_mode: str
    primary_gate: str
    secondary_gates: tuple[str, ...]
    blocked_by: tuple[str, ...]
    warnings: tuple[str, ...]
    checks: dict[str, bool]
    gate_inputs: tuple[GateInput, ...]
    invariants: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "authority_mode": self.authority_mode,
            "primary_gate": self.primary_gate,
            "secondary_gates": list(self.secondary_gates),
            "blocked_by": list(self.blocked_by),
            "warnings": list(self.warnings),
            "checks": self.checks,
            "gate_inputs": [gate.to_dict() for gate in self.gate_inputs],
            "invariants": self.invariants,
        }


@dataclass(frozen=True)
class Stage125Contract:
    stage: str = "125"
    baseline_stage: str = "124"
    title: str = "Gate25/28/29 Governor"
    purpose: str = (
        "Unify Gate25 NIE v1.0, Gate28 ASD quality, and Gate29 PNE predictive "
        "secondary gates under one deterministic release governor."
    )
    primary_authority: str = "Gate25"
    secondary_authorities: tuple[str, ...] = ("Gate28", "Gate29")
    blocked_concepts: tuple[str, ...] = (
        "Gate28 primary authority",
        "Gate29 primary authority",
        "release-gate runtime training",
        "auto-repair mutation during release",
        "live provider calls in governor",
        "direct V545/V555 package merge",
    )
    invariants: dict[str, Any] = field(default_factory=lambda: {
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "gate28_primary_authority_enabled": False,
        "gate29_primary_authority_enabled": False,
        "release_gate_runtime_training_enabled": False,
        "auto_repair_mutation_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    })

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "purpose": self.purpose,
            "primary_authority": self.primary_authority,
            "secondary_authorities": list(self.secondary_authorities),
            "blocked_concepts": list(self.blocked_concepts),
            "invariants": self.invariants,
        }
