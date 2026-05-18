from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class StudioProject:
    project_id: str
    title: str
    format: Literal["series", "novel", "webnovel", "screenplay"]
    episode_count: int
    baseline_stage: str
    privacy_mode: Literal["FEATURE_ONLY", "LOCAL_FULL_TEXT"]
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EpisodeCard:
    episode_id: str
    episode_idx: int
    title: str
    function: str
    microplot_count: int
    structural_scene_count: int
    production_scene_count_estimate: int
    payoff_debt_status: str
    agency_status: str
    attention_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EpisodeBoard:
    project_id: str
    episodes: list[EpisodeCard]
    board_status: Literal["DRAFT", "WARN", "BLOCKED", "READY"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "episodes": [episode.to_dict() for episode in self.episodes],
            "board_status": self.board_status,
        }


@dataclass(frozen=True)
class RevisionItem:
    revision_id: str
    project_id: str
    episode_id: str
    source_gate: str
    severity: Literal["INFO", "WARN", "BLOCK"]
    issue_type: str
    diagnosis: str
    recommended_action: str
    writer_decision: Literal["PENDING", "APPROVED", "REJECTED", "DEFERRED"]
    evidence_path: str
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewPackage:
    package_id: str
    project_id: str
    revision_items: list[RevisionItem]
    unresolved_block_count: int
    warn_count: int
    info_count: int
    ready_for_publishing: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "project_id": self.project_id,
            "revision_items": [item.to_dict() for item in self.revision_items],
            "unresolved_block_count": self.unresolved_block_count,
            "warn_count": self.warn_count,
            "info_count": self.info_count,
            "ready_for_publishing": self.ready_for_publishing,
        }


@dataclass(frozen=True)
class PublishingPackage:
    package_id: str
    project_id: str
    export_formats: list[str]
    includes_full_text: bool
    includes_feature_reports: bool
    includes_release_evidence: bool
    package_manifest_path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
