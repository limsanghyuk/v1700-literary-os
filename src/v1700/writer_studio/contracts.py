from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StudioPanel:
    panel_id: str
    title: str
    purpose: str
    source_stage: str
    items: tuple[dict[str, Any], ...]
    blocking_rules: tuple[str, ...] = ()

    @property
    def item_count(self) -> int:
        return len(self.items)

    def to_dict(self) -> dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "title": self.title,
            "purpose": self.purpose,
            "source_stage": self.source_stage,
            "item_count": self.item_count,
            "items": [dict(item) for item in self.items],
            "blocking_rules": list(self.blocking_rules),
        }


@dataclass(frozen=True)
class WriterStudioWorkspace:
    stage: str
    title: str
    status: str
    panels: tuple[StudioPanel, ...]
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    inherited_stages: tuple[str, ...]
    export_targets: tuple[str, ...]
    issues: tuple[str, ...] = ()

    @property
    def panel_count(self) -> int:
        return len(self.panels)

    @property
    def panel_ids(self) -> tuple[str, ...]:
        return tuple(panel.panel_id for panel in self.panels)

    def panel(self, panel_id: str) -> StudioPanel:
        for panel in self.panels:
            if panel.panel_id == panel_id:
                return panel
        raise KeyError(panel_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "title": self.title,
            "status": self.status,
            "panel_count": self.panel_count,
            "panel_ids": list(self.panel_ids),
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "inherited_stages": list(self.inherited_stages),
            "export_targets": list(self.export_targets),
            "issues": list(self.issues),
            "panels": [panel.to_dict() for panel in self.panels],
        }


@dataclass(frozen=True)
class ExportArtifact:
    artifact_id: str
    format: str
    filename: str
    content: str
    source_panel_ids: tuple[str, ...]
    checksum: str

    @property
    def byte_size(self) -> int:
        return len(self.content.encode("utf-8"))

    def to_dict(self, *, include_content: bool = False) -> dict[str, Any]:
        payload = {
            "artifact_id": self.artifact_id,
            "format": self.format,
            "filename": self.filename,
            "byte_size": self.byte_size,
            "source_panel_ids": list(self.source_panel_ids),
            "checksum": self.checksum,
        }
        if include_content:
            payload["content"] = self.content
        return payload


@dataclass(frozen=True)
class ExportBundle:
    stage: str
    status: str
    artifacts: tuple[ExportArtifact, ...]
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...] = field(default_factory=tuple)

    @property
    def artifact_count(self) -> int:
        return len(self.artifacts)

    @property
    def formats(self) -> tuple[str, ...]:
        return tuple(sorted({artifact.format for artifact in self.artifacts}))

    def to_dict(self, *, include_content: bool = False) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "artifact_count": self.artifact_count,
            "formats": list(self.formats),
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
            "artifacts": [artifact.to_dict(include_content=include_content) for artifact in self.artifacts],
        }
