from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

ExpectedStatus = Literal["PASS", "BLOCK"]
ActualStatus = Literal["PASS", "BLOCK"]


@dataclass(frozen=True)
class AdversarialCase:
    case_id: str
    case_type: str
    source_stage: str
    mutation_type: str
    expected_status: ExpectedStatus
    expected_block_reason: str | None
    episode_count: int
    payload_path: str
    invariants: dict[str, Any]
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdversarialResult:
    case_id: str
    actual_status: ActualStatus
    expected_status: ExpectedStatus
    matched_expectation: bool
    block_reason: str | None
    triggered_gate: str | None
    provider_call_count: int
    node2_raw_reveal_access: int
    evidence_path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoefficientBridgeConfig:
    source_stage: str
    coefficient_memory_path: str
    load_weight_overrides: dict[str, float]
    fatigue_threshold: float
    agency_floor: float
    payoff_default_threshold: float
    style_drift_tolerance: float
    privacy_mode: Literal["LOCAL_ONLY"]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProductionSceneMapping:
    episode_id: str
    structural_scene_count: int
    production_scene_count_estimate: int
    major_sequence_count: int
    microplot_count: int
    beat_count_estimate: int
    runtime_minutes: int
    density_status: Literal["PASS", "WARN", "BLOCK"]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
