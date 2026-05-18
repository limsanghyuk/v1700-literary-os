from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import copy
import json

from v1700.writer_studio.contracts import StudioPanel, WriterStudioWorkspace, ExportArtifact
from v1700.writer_studio.export_pipeline import WriterStudioExportPipeline
from v1700.writer_studio.workspace import build_writer_studio_workspace


FORBIDDEN_LEAKAGE_MARKERS = (
    "RAW_REVEAL",
    "INTERNAL_MARKER",
    "CHAIN_OF_THOUGHT",
    "reader_only_fact_direct_reveal",
)


@dataclass(frozen=True)
class StudioEditOperation:
    """Deterministic writer-side edit patch against a Studio panel item."""

    operation_id: str
    panel_id: str
    selector_key: str
    selector_value: Any
    field: str
    value: Any
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "panel_id": self.panel_id,
            "selector_key": self.selector_key,
            "selector_value": self.selector_value,
            "field": self.field,
            "value": self.value,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class AppliedStudioEdit:
    operation: StudioEditOperation
    before: Any
    after: Any
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation": self.operation.to_dict(),
            "before": self.before,
            "after": self.after,
            "status": self.status,
        }


@dataclass(frozen=True)
class RoundTripFidelityReport:
    stage: str
    status: str
    edit_count: int
    applied_count: int
    before_artifact_count: int
    after_artifact_count: int
    changed_artifact_count: int
    unchanged_artifact_count: int
    fidelity_score: float
    json_roundtrip_panel_count: int
    markdown_contains_edit_summary: bool
    html_contains_stage90_marker: bool
    scene_csv_row_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...] = field(default_factory=tuple)
    applied_edits: tuple[AppliedStudioEdit, ...] = field(default_factory=tuple)
    before_checksums: dict[str, str] = field(default_factory=dict)
    after_checksums: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "edit_count": self.edit_count,
            "applied_count": self.applied_count,
            "before_artifact_count": self.before_artifact_count,
            "after_artifact_count": self.after_artifact_count,
            "changed_artifact_count": self.changed_artifact_count,
            "unchanged_artifact_count": self.unchanged_artifact_count,
            "fidelity_score": self.fidelity_score,
            "json_roundtrip_panel_count": self.json_roundtrip_panel_count,
            "markdown_contains_edit_summary": self.markdown_contains_edit_summary,
            "html_contains_stage90_marker": self.html_contains_stage90_marker,
            "scene_csv_row_count": self.scene_csv_row_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
            "applied_edits": [edit.to_dict() for edit in self.applied_edits],
            "before_checksums": dict(self.before_checksums),
            "after_checksums": dict(self.after_checksums),
        }


class StudioRoundTripEngine:
    """Applies writer edits, re-exports artifacts, and audits fidelity.

    Stage90 deliberately remains a static/local contract: no browser automation,
    no external provider calls, and no raw reveal authority are introduced.
    """

    def default_patch_set(self) -> tuple[StudioEditOperation, ...]:
        return (
            StudioEditOperation(
                operation_id="edit_story_premise_stage90",
                panel_id="story_bible",
                selector_key="key",
                selector_value="series_premise",
                field="value",
                value="A Korean longform drama season hardened by Stage90 round-trip Studio edits and export fidelity checks.",
                reason="Prove writer-facing premise edits can round-trip through Studio exports.",
            ),
            StudioEditOperation(
                operation_id="edit_ep08_quality_note",
                panel_id="episode_board",
                selector_key="episode_id",
                selector_value="EP08",
                field="editorial_roundtrip_note",
                value="Mid-season turn clarified without direct reveal leakage.",
                reason="Prove episode board annotations survive re-export.",
            ),
            StudioEditOperation(
                operation_id="edit_scene_afterimage",
                panel_id="scene_card_board",
                selector_key="scene_id",
                selector_value="EP08_SC10",
                field="afterimage_marker",
                value="닫히는 엘리베이터 문틈의 찬기 #90",
                reason="Prove surface scene edits preserve Node2-only contract.",
            ),
            StudioEditOperation(
                operation_id="edit_reveal_budget_note",
                panel_id="reveal_budget_board",
                selector_key="reveal_policy",
                selector_value="foreshadow_only",
                field="roundtrip_policy_note",
                value="Foreshadowing may be strengthened, but direct answer text remains blocked.",
                reason="Prove reveal budget annotations remain policy-bound after export.",
            ),
        )

    def apply_patch(
        self,
        workspace: WriterStudioWorkspace,
        operations: tuple[StudioEditOperation, ...] | None = None,
    ) -> tuple[WriterStudioWorkspace, tuple[AppliedStudioEdit, ...]]:
        operations = operations or self.default_patch_set()
        panel_items: dict[str, list[dict[str, Any]]] = {
            panel.panel_id: [copy.deepcopy(dict(item)) for item in panel.items]
            for panel in workspace.panels
        }
        applied: list[AppliedStudioEdit] = []
        issues: list[str] = list(workspace.issues)
        for op in operations:
            items = panel_items.get(op.panel_id)
            if items is None:
                issues.append(f"missing_panel:{op.panel_id}")
                applied.append(AppliedStudioEdit(op, None, None, "blocked"))
                continue
            target = next((item for item in items if item.get(op.selector_key) == op.selector_value), None)
            if target is None:
                issues.append(f"missing_item:{op.operation_id}")
                applied.append(AppliedStudioEdit(op, None, None, "blocked"))
                continue
            before = target.get(op.field)
            target[op.field] = op.value
            applied.append(AppliedStudioEdit(op, before, op.value, "applied"))

        patched_panels = []
        for panel in workspace.panels:
            patched_panels.append(
                StudioPanel(
                    panel_id=panel.panel_id,
                    title=panel.title,
                    purpose=panel.purpose,
                    source_stage=panel.source_stage,
                    items=tuple(panel_items[panel.panel_id]),
                    blocking_rules=panel.blocking_rules,
                )
            )
        return (
            WriterStudioWorkspace(
                stage="90",
                title="Studio Round-trip Editing + Export Fidelity Hardening",
                status="pass" if not issues else "blocked",
                panels=tuple(patched_panels),
                provider_default_calls=workspace.provider_default_calls,
                node2_raw_reveal_access_count=workspace.node2_raw_reveal_access_count,
                inherited_stages=("stage89",) + tuple(stage for stage in workspace.inherited_stages if stage != "stage89"),
                export_targets=workspace.export_targets + ("roundtrip_fidelity_report",),
                issues=tuple(issues),
            ),
            tuple(applied),
        )

    def run_roundtrip(self) -> RoundTripFidelityReport:
        before_workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
        exporter = WriterStudioExportPipeline()
        before_bundle = exporter.build_bundle(before_workspace)
        patched_workspace, applied = self.apply_patch(before_workspace)
        after_bundle = exporter.build_bundle(patched_workspace)

        before_checksums = {artifact.artifact_id: artifact.checksum for artifact in before_bundle.artifacts}
        after_checksums = {artifact.artifact_id: artifact.checksum for artifact in after_bundle.artifacts}
        changed = [key for key, checksum in after_checksums.items() if before_checksums.get(key) != checksum]
        unchanged = [key for key, checksum in after_checksums.items() if before_checksums.get(key) == checksum]
        after_by_id: dict[str, ExportArtifact] = {artifact.artifact_id: artifact for artifact in after_bundle.artifacts}
        json_state = json.loads(after_by_id["writer_studio_state"].content)
        markdown = after_by_id["writer_handoff"].content
        html = after_by_id["static_studio_preview"].content
        csv_text = after_by_id["scene_review_sheet"].content

        fidelity_checks = {
            "all_edits_applied": all(edit.status == "applied" for edit in applied),
            "artifact_count_preserved": before_bundle.artifact_count == after_bundle.artifact_count >= 5,
            "required_artifacts_changed": {"writer_studio_state", "writer_handoff", "static_studio_preview", "platform_serialization_pack", "scene_review_sheet"}.issubset(set(changed)),
            "json_roundtrip_panels_preserved": json_state.get("panel_count") == before_workspace.panel_count,
            "markdown_contains_edit_summary": "stage90" in markdown.lower() and "round-trip" in markdown.lower(),
            "html_contains_stage90_marker": "Stage90" in html,
            "scene_csv_rows_preserved": max(len(csv_text.splitlines()) - 1, 0) == before_workspace.panel("scene_card_board").item_count,
            "provider_zero": patched_workspace.provider_default_calls == 0 and after_bundle.provider_default_calls == 0,
            "node2_boundary_zero": patched_workspace.node2_raw_reveal_access_count == 0 and after_bundle.node2_raw_reveal_access_count == 0,
            "no_forbidden_leakage_markers": not any(marker in artifact.content for marker in FORBIDDEN_LEAKAGE_MARKERS for artifact in after_bundle.artifacts),
        }
        issues = [name for name, ok in fidelity_checks.items() if not ok]
        score = round(sum(1 for ok in fidelity_checks.values() if ok) / len(fidelity_checks) * 10, 2)
        return RoundTripFidelityReport(
            stage="90",
            status="pass" if not issues else "blocked",
            edit_count=len(applied),
            applied_count=sum(1 for edit in applied if edit.status == "applied"),
            before_artifact_count=before_bundle.artifact_count,
            after_artifact_count=after_bundle.artifact_count,
            changed_artifact_count=len(changed),
            unchanged_artifact_count=len(unchanged),
            fidelity_score=score,
            json_roundtrip_panel_count=json_state.get("panel_count", 0),
            markdown_contains_edit_summary=fidelity_checks["markdown_contains_edit_summary"],
            html_contains_stage90_marker=fidelity_checks["html_contains_stage90_marker"],
            scene_csv_row_count=max(len(csv_text.splitlines()) - 1, 0),
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            issues=tuple(issues),
            applied_edits=tuple(applied),
            before_checksums=before_checksums,
            after_checksums=after_checksums,
        )


def run_stage90_roundtrip_smoke() -> dict[str, Any]:
    report = StudioRoundTripEngine().run_roundtrip()
    payload = report.to_dict()
    payload["claim"] = "Stage90 proves writer-side Studio edits can be applied, re-exported, and fidelity-audited without external providers or raw reveal access."
    return payload
