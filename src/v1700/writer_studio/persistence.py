from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from v1700.writer_studio.contracts import StudioPanel, WriterStudioWorkspace
from v1700.writer_studio.roundtrip import StudioRoundTripEngine


@dataclass(frozen=True)
class StudioPersistenceSnapshot:
    snapshot_id: str
    sequence: int
    reason: str
    workspace_stage: str
    panel_count: int
    item_count: int
    review_queue_size: int
    event_count: int
    checksum: str
    payload: dict[str, Any]

    def to_dict(self, *, include_payload: bool = False) -> dict[str, Any]:
        data = {
            "snapshot_id": self.snapshot_id,
            "sequence": self.sequence,
            "reason": self.reason,
            "workspace_stage": self.workspace_stage,
            "panel_count": self.panel_count,
            "item_count": self.item_count,
            "review_queue_size": self.review_queue_size,
            "event_count": self.event_count,
            "checksum": self.checksum,
        }
        if include_payload:
            data["payload"] = self.payload
        return data


class StudioPersistenceStore:
    """Deterministic in-memory persistence layer for Writer Studio state.

    Stage91 deliberately models persistence as a portable snapshot contract rather
    than a database server. This keeps provider_default_calls at 0 and makes event
    replay reproducible inside tests, release gates, and ZIP probes.
    """

    def __init__(self) -> None:
        self._snapshots: list[StudioPersistenceSnapshot] = []

    @property
    def snapshots(self) -> tuple[StudioPersistenceSnapshot, ...]:
        return tuple(self._snapshots)

    def persist(
        self,
        workspace: WriterStudioWorkspace,
        *,
        sequence: int,
        reason: str,
        review_queue_size: int,
        event_count: int,
    ) -> StudioPersistenceSnapshot:
        payload = workspace.to_dict()
        text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        checksum = hashlib.sha256(text.encode("utf-8")).hexdigest().upper()
        item_count = sum(panel.item_count for panel in workspace.panels)
        snapshot = StudioPersistenceSnapshot(
            snapshot_id=f"stage91_snapshot_{sequence:03d}",
            sequence=sequence,
            reason=reason,
            workspace_stage=workspace.stage,
            panel_count=workspace.panel_count,
            item_count=item_count,
            review_queue_size=review_queue_size,
            event_count=event_count,
            checksum=checksum,
            payload=payload,
        )
        self._snapshots.append(snapshot)
        return snapshot

    def latest(self) -> StudioPersistenceSnapshot:
        if not self._snapshots:
            raise LookupError("no_persistence_snapshots")
        return self._snapshots[-1]


def clone_workspace_with_stage91_metadata(
    workspace: WriterStudioWorkspace,
    *,
    title: str = "Studio Persistence + Review Queue + UI Event Replay",
) -> WriterStudioWorkspace:
    return WriterStudioWorkspace(
        stage="91",
        title=title,
        status=workspace.status,
        panels=workspace.panels,
        provider_default_calls=workspace.provider_default_calls,
        node2_raw_reveal_access_count=workspace.node2_raw_reveal_access_count,
        inherited_stages=("stage90",) + tuple(stage for stage in workspace.inherited_stages if stage != "stage90"),
        export_targets=workspace.export_targets + ("persistence_snapshot", "review_queue", "ui_event_replay_log"),
        issues=workspace.issues,
    )


def build_stage91_base_workspace() -> WriterStudioWorkspace:
    base = StudioRoundTripEngine().run_roundtrip()
    # The roundtrip report proves Stage90 edits; rebuild the patched workspace so
    # Stage91 can persist the actual Studio state rather than only the report.
    builder = StudioRoundTripEngine()
    before = __import__("v1700.writer_studio.workspace", fromlist=["build_writer_studio_workspace"]).build_writer_studio_workspace(
        episode_count=16,
        scenes_per_episode=10,
    )
    patched, _ = builder.apply_patch(before)
    workspace = clone_workspace_with_stage91_metadata(patched)
    if base.status != "pass":
        panels = tuple(
            StudioPanel(
                panel_id=panel.panel_id,
                title=panel.title,
                purpose=panel.purpose,
                source_stage=panel.source_stage,
                items=panel.items,
                blocking_rules=panel.blocking_rules,
            )
            for panel in workspace.panels
        )
        workspace = WriterStudioWorkspace(
            stage="91",
            title=workspace.title,
            status="blocked",
            panels=panels,
            provider_default_calls=workspace.provider_default_calls,
            node2_raw_reveal_access_count=workspace.node2_raw_reveal_access_count,
            inherited_stages=workspace.inherited_stages,
            export_targets=workspace.export_targets,
            issues=workspace.issues + ("stage90_roundtrip_not_pass",),
        )
    return workspace


def patch_workspace_item(
    workspace: WriterStudioWorkspace,
    *,
    panel_id: str,
    selector_key: str,
    selector_value: Any,
    field: str,
    value: Any,
) -> WriterStudioWorkspace:
    panel_items: dict[str, list[dict[str, Any]]] = {
        panel.panel_id: [copy.deepcopy(dict(item)) for item in panel.items]
        for panel in workspace.panels
    }
    issues = list(workspace.issues)
    target_items = panel_items.get(panel_id)
    if target_items is None:
        issues.append(f"missing_panel:{panel_id}")
    else:
        target = next((item for item in target_items if item.get(selector_key) == selector_value), None)
        if target is None:
            issues.append(f"missing_item:{panel_id}:{selector_value}")
        else:
            target[field] = value

    panels = tuple(
        StudioPanel(
            panel_id=panel.panel_id,
            title=panel.title,
            purpose=panel.purpose,
            source_stage=panel.source_stage,
            items=tuple(panel_items[panel.panel_id]),
            blocking_rules=panel.blocking_rules,
        )
        for panel in workspace.panels
    )
    return WriterStudioWorkspace(
        stage="91",
        title=workspace.title,
        status="pass" if not issues else "blocked",
        panels=panels,
        provider_default_calls=workspace.provider_default_calls,
        node2_raw_reveal_access_count=workspace.node2_raw_reveal_access_count,
        inherited_stages=workspace.inherited_stages,
        export_targets=workspace.export_targets,
        issues=tuple(issues),
    )
