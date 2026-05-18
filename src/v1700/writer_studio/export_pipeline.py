from __future__ import annotations

import csv
import hashlib
import html
import io
import json

from v1700.writer_studio.contracts import ExportArtifact, ExportBundle, WriterStudioWorkspace
from v1700.writer_studio.workspace import build_writer_studio_workspace


class WriterStudioExportPipeline:
    """Deterministic, provider-zero export pipeline for Writer Studio stages."""

    def build_bundle(self, workspace: WriterStudioWorkspace | None = None) -> ExportBundle:
        workspace = workspace or build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
        prefix = f"stage{workspace.stage}"
        artifacts = (
            self._artifact("writer_studio_state", "json", f"{prefix}_writer_studio_state.json", json.dumps(workspace.to_dict(), ensure_ascii=False, indent=2), workspace.panel_ids),
            self._artifact("writer_handoff", "markdown", f"{prefix}_writer_handoff.md", self._render_markdown(workspace), workspace.panel_ids),
            self._artifact("static_studio_preview", "html", f"{prefix}_writer_studio_preview.html", self._render_html(workspace), workspace.panel_ids),
            self._artifact("platform_serialization_pack", "platform_serialization_pack", f"{prefix}_platform_serialization_pack.md", self._render_platform_pack(workspace), ("episode_board", "scene_card_board", "reveal_budget_board")),
            self._artifact("scene_review_sheet", "scene_csv", f"{prefix}_scene_review_sheet.csv", self._render_scene_csv(workspace), ("scene_card_board", "character_knowledge_board", "reveal_budget_board")),
        )
        issues = self._validate(workspace, artifacts)
        return ExportBundle(
            stage=workspace.stage,
            status="pass" if not issues else "blocked",
            artifacts=artifacts,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            issues=tuple(issues),
        )

    def _artifact(self, artifact_id: str, fmt: str, filename: str, content: str, panel_ids: tuple[str, ...]) -> ExportArtifact:
        final_content = content if content.endswith("\n") else content + "\n"
        checksum = hashlib.sha256(final_content.encode("utf-8")).hexdigest().upper()
        return ExportArtifact(
            artifact_id=artifact_id,
            format=fmt,
            filename=filename,
            content=final_content,
            source_panel_ids=panel_ids,
            checksum=checksum,
        )

    def _render_markdown(self, workspace: WriterStudioWorkspace) -> str:
        lines = [
            f"# Stage{workspace.stage} Writer Studio Handoff",
            f"- Title: {workspace.title}",
            "",
            f"- Status: `{workspace.status}`",
            "- Provider default calls: `0`",
            "- Node2 raw reveal access: `0`",
            "",
            "## Panels",
            "",
        ]
        for panel in workspace.panels:
            lines.extend([
                f"### {panel.title}",
                "",
                f"- Panel ID: `{panel.panel_id}`",
                f"- Source stage: `{panel.source_stage}`",
                f"- Purpose: {panel.purpose}",
                f"- Item count: `{panel.item_count}`",
                "",
            ])
        lines.extend([
            "## Export Targets",
            "",
            *[f"- `{target}`" for target in workspace.export_targets],
            "",
            "## Inherited Lineage",
            "",
            *[f"- `{stage}`" for stage in workspace.inherited_stages],
        ])
        return "\n".join(lines)

    def _render_html(self, workspace: WriterStudioWorkspace) -> str:
        cards = []
        for panel in workspace.panels:
            items = "".join(f"<li>{html.escape(json.dumps(item, ensure_ascii=False))}</li>" for item in panel.items[:5])
            cards.append(
                f"<section class='panel'><h2>{html.escape(panel.title)}</h2>"
                f"<p>{html.escape(panel.purpose)}</p>"
                f"<p><strong>Source:</strong> {html.escape(panel.source_stage)} | "
                f"<strong>Items:</strong> {panel.item_count}</p><ul>{items}</ul></section>"
            )
        return "".join([
            "<!doctype html><html lang='ko'><head><meta charset='utf-8'>",
            f"<title>V1700 Stage{workspace.stage} Writer Studio</title>",
            "<style>body{font-family:system-ui,sans-serif;margin:2rem;line-height:1.5}.panel{border:1px solid #ddd;border-radius:12px;padding:1rem;margin:1rem 0}code{background:#f6f6f6;padding:.1rem .25rem}</style>",
            "</head><body>",
            f"<h1>V1700 Stage{workspace.stage} Writer Studio</h1>",
            f"<p>Status: <code>{workspace.status}</code> · Provider default calls: <code>0</code> · Node2 raw reveal access: <code>0</code></p>",
            *cards,
            "</body></html>",
        ])

    def _render_platform_pack(self, workspace: WriterStudioWorkspace) -> str:
        episode_board = workspace.panel("episode_board")
        scene_board = workspace.panel("scene_card_board")
        lines = [f"# Stage{workspace.stage} Platform Serialization Pack", ""]
        for episode in episode_board.items:
            lines.append(f"## {episode['episode_id']} · {episode['act']}")
            lines.append(f"- Scene count: {episode['scene_count']}")
            lines.append(f"- Average quality: {episode['average_quality']}")
            lines.append("")
        lines.append("## Representative Scene Cards")
        lines.append("")
        for scene in scene_board.items:
            lines.append(f"- `{scene['scene_id']}`: {scene['afterimage_marker']} / {scene['reveal_policy']} / {scene['knowledge_mode']}")
        return "\n".join(lines)

    def _render_scene_csv(self, workspace: WriterStudioWorkspace) -> str:
        scene_board = workspace.panel("scene_card_board")
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["scene_id", "episode_id", "act", "reveal_policy", "knowledge_mode", "afterimage_marker", "surface_contract"])
        writer.writeheader()
        for scene in scene_board.items:
            writer.writerow(scene)
        return output.getvalue()

    def _validate(self, workspace: WriterStudioWorkspace, artifacts: tuple[ExportArtifact, ...]) -> list[str]:
        issues: list[str] = []
        if workspace.status != "pass":
            issues.append("writer_studio_workspace_not_pass")
        required_formats = {"markdown", "json", "html", "platform_serialization_pack", "scene_csv"}
        if not required_formats.issubset({artifact.format for artifact in artifacts}):
            issues.append("missing_required_export_format")
        if len(artifacts) < 5:
            issues.append("export_artifact_count_below_5")
        if any(not artifact.checksum or artifact.byte_size == 0 for artifact in artifacts):
            issues.append("empty_export_artifact_or_checksum")
        if workspace.provider_default_calls != 0:
            issues.append("provider_default_calls_not_zero")
        if workspace.node2_raw_reveal_access_count != 0:
            issues.append("node2_raw_reveal_access_not_zero")
        return issues


def run_stage89_export_pipeline_smoke() -> dict:
    workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
    bundle = WriterStudioExportPipeline().build_bundle(workspace)
    payload = bundle.to_dict(include_content=False)
    payload["workspace"] = workspace.to_dict()
    payload["claim"] = "Stage89 exports writer-facing Studio state to Markdown, JSON, static HTML, platform pack, and scene CSV without external providers."
    return payload
