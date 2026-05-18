from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

AbsorptionStatus = Literal["ACCEPT", "WRAP_ONLY", "REJECT", "DEFER", "BLOCK"]
RiskLevel = Literal["LOW", "MEDIUM", "HIGH", "BLOCK"]
BridgeStatus = Literal["PASS", "WARN", "BLOCK"]

@dataclass(frozen=True)
class V485AbsorptionCandidate:
    candidate_id: str
    source_component: str
    source_version_label: str
    target_v1700_module: str
    absorption_status: AbsorptionStatus
    risk_level: RiskLevel
    requires_sandbox: bool
    requires_redaction: bool
    requires_release_gate_trace: bool
    rationale: str = ""
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class V485VersionDriftReport:
    package_label: str
    readme_version: str
    pyproject_version: str
    manifest_version: str
    live_manifest_version: str
    release_gate_version: str
    drift_detected: bool
    release_block: bool
    direct_metadata_import_allowed: bool = False
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class AdapterBridgeProbeResult:
    bridge_id: str
    source_adapter_pattern: str
    target_adapter: str
    provider_call_mode: Literal["FIXTURE", "SANDBOX_LIVE", "DISABLED"]
    credential_included: bool
    raw_manuscript_included: bool
    raw_response_stored: bool
    response_normalizer_required: bool
    bridge_status: BridgeStatus
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class ScenePipelineBridgeResult:
    bridge_id: str
    source_pipeline: str
    target_mode: Literal["PROSE", "SCENARIO", "DRAMA"]
    provider_call_mode: Literal["FIXTURE", "SANDBOX_LIVE", "DISABLED"]
    raw_manuscript_included: bool
    raw_response_stored: bool
    normalized_scene_count: int
    writer_decision_required: bool
    bridge_status: BridgeStatus
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class DramaEpisodeBridgeResult:
    episode_plan_id: str
    episode_count: int
    scene_count: int
    provider_mode: str
    writer_decision_required: bool
    review_queue_items: int
    export_ready: bool
    status: BridgeStatus
    def to_dict(self) -> dict:
        return asdict(self)
