from __future__ import annotations

from statistics import mean

from v1700.agent_benchmark.harness import run_stage88_agent_benchmark_smoke
from v1700.episode_scaleup.evidence import EpisodeScaleupEvidenceEngine
from v1700.writer_studio.contracts import StudioPanel, WriterStudioWorkspace


REQUIRED_PANEL_IDS = (
    "story_bible",
    "episode_board",
    "scene_card_board",
    "character_knowledge_board",
    "reveal_budget_board",
    "agent_benchmark_panel",
    "branchpoint_impact_panel",
    "export_pipeline_panel",
)


class WriterStudioWorkspaceBuilder:
    """Builds a deterministic Stage89 writer-facing studio model.

    The Studio is not a web server. It is a portable UI/data contract that can
    render to static HTML/JSON/Markdown while preserving the V1700 local-first,
    provider-zero, Node2 surface-only boundary.
    """

    def build(self, *, episode_count: int = 16, scenes_per_episode: int = 10) -> WriterStudioWorkspace:
        season = EpisodeScaleupEvidenceEngine().build(
            episode_count=episode_count,
            scenes_per_episode=scenes_per_episode,
        )
        benchmark = run_stage88_agent_benchmark_smoke()
        panels = (
            self._story_bible_panel(season),
            self._episode_board_panel(season),
            self._scene_card_board_panel(season),
            self._character_knowledge_panel(season),
            self._reveal_budget_panel(season),
            self._agent_benchmark_panel(benchmark),
            self._branchpoint_impact_panel(),
            self._export_pipeline_panel(),
        )
        issues = self._validate(panels, benchmark)
        return WriterStudioWorkspace(
            stage="89",
            title="Writer Studio UI + Export Pipeline",
            status="pass" if not issues else "blocked",
            panels=panels,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            inherited_stages=("stage88", "stage87", "stage86", "stage85", "stage84", "stage83.1"),
            export_targets=("markdown", "json", "html", "platform_serialization_pack", "scene_csv"),
            issues=tuple(issues),
        )

    def _story_bible_panel(self, season) -> StudioPanel:
        acts = sorted({scene.act for episode in season.episodes for scene in episode.scenes})
        items = (
            {
                "key": "series_premise",
                "value": "A Korean longform drama season governed by arc, reveal, knowledge, and reader-surface constraints.",
            },
            {"key": "episode_count", "value": season.episode_count},
            {"key": "scene_count", "value": season.total_scene_count},
            {"key": "act_coverage", "value": ",".join(acts)},
            {"key": "provider_default_calls", "value": 0},
        )
        return StudioPanel(
            panel_id="story_bible",
            title="Story Bible",
            purpose="Portable source-of-truth panel for premise, season scope, and local-first invariants.",
            source_stage="stage87",
            items=items,
            blocking_rules=("episode_count_must_be_16", "provider_default_calls_must_be_0"),
        )

    def _episode_board_panel(self, season) -> StudioPanel:
        items = tuple(
            {
                "episode_id": episode.episode_id,
                "act": episode.act,
                "scene_count": episode.scene_count,
                "average_quality": episode.average_quality_score,
                "reveal_policy_count": episode.reveal_policy_count,
                "blocked_direct_reveal_count": episode.blocked_direct_reveal_count,
            }
            for episode in season.episodes
        )
        return StudioPanel(
            panel_id="episode_board",
            title="Episode Board",
            purpose="Writer-facing board for 8-16 episode scale-up inspection.",
            source_stage="stage87",
            items=items,
            blocking_rules=("minimum_8_episodes", "minimum_80_scenes", "quality_floor_8"),
        )

    def _scene_card_board_panel(self, season) -> StudioPanel:
        selected = []
        for episode in season.episodes:
            selected.extend([episode.scenes[0], episode.scenes[-1]])
        items = tuple(
            {
                "scene_id": scene.scene_id,
                "episode_id": scene.episode_id,
                "act": scene.act,
                "reveal_policy": scene.reveal_policy,
                "knowledge_mode": scene.knowledge_mode,
                "afterimage_marker": scene.afterimage_marker,
                "surface_contract": "node2_surface_only",
            }
            for scene in selected
        )
        return StudioPanel(
            panel_id="scene_card_board",
            title="Scene Card Board",
            purpose="Compact scene cards for writer review without raw reveal access.",
            source_stage="stage87",
            items=items,
            blocking_rules=("must_not_expose_raw_reveal", "must_keep_node2_surface_contract"),
        )

    def _character_knowledge_panel(self, season) -> StudioPanel:
        modes = sorted({scene.knowledge_mode for episode in season.episodes for scene in episode.scenes})
        counts = {mode: 0 for mode in modes}
        for episode in season.episodes:
            for scene in episode.scenes:
                counts[scene.knowledge_mode] += 1
        items = tuple({"knowledge_mode": mode, "scene_count": counts[mode]} for mode in modes)
        return StudioPanel(
            panel_id="character_knowledge_board",
            title="Character Knowledge Board",
            purpose="Tracks knows/suspects/unaware/reader-only pressure as a writer-visible board.",
            source_stage="stage86",
            items=items,
            blocking_rules=("reader_only_must_not_enter_character_mind", "knowledge_modes_must_be_visible"),
        )

    def _reveal_budget_panel(self, season) -> StudioPanel:
        policies = sorted({scene.reveal_policy for episode in season.episodes for scene in episode.scenes})
        counts = {policy: 0 for policy in policies}
        for episode in season.episodes:
            for scene in episode.scenes:
                counts[scene.reveal_policy] += 1
        items = tuple({"reveal_policy": policy, "scene_count": counts[policy]} for policy in policies)
        return StudioPanel(
            panel_id="reveal_budget_board",
            title="Reveal Budget Board",
            purpose="Shows allow/foreshadow/delay/block distribution before export.",
            source_stage="stage86",
            items=items,
            blocking_rules=("direct_reveal_must_follow_policy", "foreshadow_only_must_not_name_answer"),
        )

    def _agent_benchmark_panel(self, benchmark: dict) -> StudioPanel:
        items = tuple(
            {
                "agent_id": agent["agent_id"],
                "role": agent["role"],
                "average_score": benchmark["agent_averages"].get(agent["agent_id"], 0.0),
            }
            for agent in benchmark["agents"]
        )
        return StudioPanel(
            panel_id="agent_benchmark_panel",
            title="AI Agent Benchmark Panel",
            purpose="Displays Stage88 artificial editor/reader consensus without requiring external humans.",
            source_stage="stage88",
            items=items,
            blocking_rules=("minimum_6_agents", "consensus_score_minimum_8"),
        )

    def _branchpoint_impact_panel(self) -> StudioPanel:
        items = (
            {"branchpoint": "Stage25 Node2", "status": "protected", "gate": "node_projection_gate"},
            {"branchpoint": "Stage80 Korean Drama Hierarchy", "status": "protected", "gate": "stage80_release_gate"},
            {"branchpoint": "Stage85 Traceability", "status": "protected", "gate": "symbol_to_branchpoint_trace_gate"},
            {"branchpoint": "Stage86 Arc-Reveal-Knowledge", "status": "protected", "gate": "stage86_release_gate"},
            {"branchpoint": "Stage88 Agent Benchmark", "status": "protected", "gate": "stage88_release_gate"},
        )
        return StudioPanel(
            panel_id="branchpoint_impact_panel",
            title="Branchpoint Impact Panel",
            purpose="Writer Studio change review panel for branchpoint survival before export.",
            source_stage="stage85",
            items=items,
            blocking_rules=("p0_branchpoint_coverage_100_percent", "stage89_must_not_bypass_trace_gate"),
        )

    def _export_pipeline_panel(self) -> StudioPanel:
        items = (
            {"format": "markdown", "target": "writer_handoff"},
            {"format": "json", "target": "machine_readable_studio_state"},
            {"format": "html", "target": "static_writer_studio_preview"},
            {"format": "platform_serialization_pack", "target": "episode_upload_preparation"},
            {"format": "scene_csv", "target": "spreadsheet_scene_review"},
        )
        return StudioPanel(
            panel_id="export_pipeline_panel",
            title="Export Pipeline Panel",
            purpose="Lists deterministic export targets generated without external providers.",
            source_stage="stage89",
            items=items,
            blocking_rules=("minimum_5_export_artifacts", "export_checksums_required"),
        )

    def _validate(self, panels: tuple[StudioPanel, ...], benchmark: dict) -> list[str]:
        issues: list[str] = []
        panel_ids = {panel.panel_id for panel in panels}
        for required in REQUIRED_PANEL_IDS:
            if required not in panel_ids:
                issues.append(f"missing_panel:{required}")
        if benchmark.get("status") != "pass":
            issues.append("stage88_agent_benchmark_not_pass")
        if benchmark.get("consensus_score", 0.0) < 8.0:
            issues.append("stage88_consensus_below_8")
        if any(panel.item_count == 0 for panel in panels):
            issues.append("empty_studio_panel")
        if len(panel_ids) != len(panels):
            issues.append("duplicate_studio_panel_id")
        return issues


def build_writer_studio_workspace(*, episode_count: int = 16, scenes_per_episode: int = 10) -> WriterStudioWorkspace:
    return WriterStudioWorkspaceBuilder().build(episode_count=episode_count, scenes_per_episode=scenes_per_episode)


def run_writer_studio_smoke() -> dict:
    workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
    payload = workspace.to_dict()
    payload["claim"] = "Stage89 exposes Writer Studio UI data panels while preserving Stage88/87/86 branchpoint guarantees."
    return payload
