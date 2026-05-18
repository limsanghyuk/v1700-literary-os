from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Status = Literal["pass", "warn", "blocked"]
Mode = Literal["PROSE", "SCENARIO", "REVIEW"]
PrivacyMode = Literal["FEATURE_ONLY", "LOCAL_FULL_TEXT"]
DecisionState = Literal["PENDING", "APPROVED", "REJECTED", "DEFERRED", "APPLIED"]


@dataclass(frozen=True)
class StudioBetaProject:
    project_id: str
    title: str
    project_type: Literal["novel", "webnovel", "screenplay", "series"]
    privacy_mode: PrivacyMode
    active_mode: Mode
    baseline_stage: str
    feature_only: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StudioSession:
    session_id: str
    project_id: str
    opened_at: str
    active_episode_id: str
    active_scene_id: str
    unsaved_changes: bool
    provider_call_count: int = 0
    live_provider_call_count_in_release_gate: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SceneCard:
    scene_id: str
    episode_id: str
    title: str
    mode: Mode
    intent: str
    beat_count: int
    has_raw_manuscript: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkspaceState:
    project_id: str
    episodes: tuple[str, ...]
    scene_cards: tuple[SceneCard, ...]
    revision_queue_size: int
    unresolved_block_count: int
    export_ready: bool
    raw_manuscript_provider_leakage: int = 0
    node2_raw_reveal_access: int = 0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["scene_cards"] = [card.to_dict() for card in self.scene_cards]
        return payload


@dataclass(frozen=True)
class BoardReport:
    status: Status
    board_id: str
    mode: Mode
    cards: tuple[dict[str, Any], ...]
    provider_call_count: int = 0
    raw_manuscript_provider_leakage: int = 0
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WriterDecision:
    decision_id: str
    revision_id: str
    decision: DecisionState
    reason: str
    approved_by_writer: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RevisionApplyGuardResult:
    status: Status
    applied_revision_count: int
    blocked_revision_count: int
    writer_approval_required: bool
    unauthorized_apply_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StudioBetaExportManifest:
    status: Status
    export_id: str
    project_id: str
    includes_full_text: bool
    includes_feature_reports: bool
    includes_release_evidence: bool
    workspace_snapshot_path: str
    writer_handoff_path: str
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalTelemetryReport:
    status: Status
    event_count: int
    raw_manuscript_included: bool
    credential_included: bool
    provider_payload_included: bool
    local_only: bool
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
