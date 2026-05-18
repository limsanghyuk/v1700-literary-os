from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Status = Literal["PASS", "BLOCK"]
Severity = Literal["INFO", "WARN", "BLOCK", "CRITICAL_BLOCK"]


@dataclass(frozen=True)
class NIEAdversarialCase:
    """Machine-readable expected-failure contract for Stage119.

    Stage119 intentionally mutates NIE/NIL evidence rather than generated prose.
    Each BLOCK case must identify the exact gate family that should reject it so
    release checks prove broken intelligence loops do not silently pass.
    """

    case_id: str
    case_type: str
    mutation_type: str
    expected_status: Status
    expected_block_reason: str | None
    expected_triggered_gate: str | None
    severity: Severity
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_type": self.case_type,
            "mutation_type": self.mutation_type,
            "expected_status": self.expected_status,
            "expected_block_reason": self.expected_block_reason,
            "expected_triggered_gate": self.expected_triggered_gate,
            "severity": self.severity,
            "payload": self.payload,
        }


@dataclass(frozen=True)
class NIEAdversarialResult:
    case_id: str
    case_type: str
    mutation_type: str
    expected_status: Status
    actual_status: Status
    matched_expectation: bool
    block_reason: str | None
    triggered_gate: str | None
    severity: Severity
    evidence_path: str
    provider_call_count: int = 0
    physics_reward_bridge_llm_call_count: int = 0
    mae_live_provider_call_count: int = 0
    query_classifier_llm_call_count: int = 0
    node2_raw_reveal_access: int = 0
    raw_manuscript_provider_leakage: int = 0
    credential_leakage: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_type": self.case_type,
            "mutation_type": self.mutation_type,
            "expected_status": self.expected_status,
            "actual_status": self.actual_status,
            "matched_expectation": self.matched_expectation,
            "block_reason": self.block_reason,
            "triggered_gate": self.triggered_gate,
            "severity": self.severity,
            "evidence_path": self.evidence_path,
            "provider_call_count": self.provider_call_count,
            "physics_reward_bridge_llm_call_count": self.physics_reward_bridge_llm_call_count,
            "mae_live_provider_call_count": self.mae_live_provider_call_count,
            "query_classifier_llm_call_count": self.query_classifier_llm_call_count,
            "node2_raw_reveal_access": self.node2_raw_reveal_access,
            "raw_manuscript_provider_leakage": self.raw_manuscript_provider_leakage,
            "credential_leakage": self.credential_leakage,
        }
