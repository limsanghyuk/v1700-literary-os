from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from v1700.blind_critic import run_blind_critic_benchmark
from v1700.drama_composition import KoreanDramaCompositionEngine
from v1700.quality_endurance.engine import QualityEnduranceEngine


DEFAULT_PROMPT = "낮은 위치의 인물이 제도, 추방, 귀환을 통과하며 자기 역할을 완성하는 한국 드라마"


@dataclass(frozen=True)
class EpisodeDraft:
    episode_id: str
    title: str
    macro_plot_id: str
    whole_story_progress: str
    scene_count: int
    markdown: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "title": self.title,
            "macro_plot_id": self.macro_plot_id,
            "whole_story_progress": self.whole_story_progress,
            "scene_count": self.scene_count,
            "markdown": self.markdown,
        }


class CommercialLongformReleaseEngine:
    """Stage83 commercial longform release candidate assembler.

    This is not a paid-provider execution path. It assembles a reproducible
    local-first commercial candidate evidence pack: three generated episode
    files, actual-text quality report, revision trace, and blind critic report.
    """

    def __init__(self) -> None:
        self.composer = KoreanDramaCompositionEngine()
        self.quality = QualityEnduranceEngine()

    def run(self, root: Path | None = None, prompt: str = DEFAULT_PROMPT) -> dict[str, Any]:
        root = root or Path(__file__).resolve().parents[3]
        project_dir = root / "sample_longform_project_01"
        project_dir.mkdir(parents=True, exist_ok=True)

        composition = self.composer.compose(prompt)
        quality_report = self.quality.run(prompt, scene_limit=30).to_dict()
        blind_report = run_blind_critic_benchmark(prompt)
        episode_drafts = self._build_episode_drafts(composition, quality_report["traces"][:30])

        episode_paths: list[str] = []
        for index, draft in enumerate(episode_drafts, start=1):
            path = project_dir / f"generated_episode_{index:02d}.md"
            path.write_text(draft.markdown, encoding="utf-8")
            episode_paths.append(str(path.relative_to(root)))

        quality_path = project_dir / "quality_report.json"
        quality_path.write_text(json.dumps(quality_report, ensure_ascii=False, indent=2), encoding="utf-8")
        refinement_path = project_dir / "refinement_trace.json"
        refinement_path.write_text(json.dumps({"traces": quality_report["traces"]}, ensure_ascii=False, indent=2), encoding="utf-8")
        blind_path = project_dir / "blind_eval_report.md"
        blind_path.write_text(self._blind_report_markdown(blind_report), encoding="utf-8")

        manifest = {
            "stage": "83",
            "title": "Commercial Longform Release Candidate",
            "prompt": prompt,
            "project_dir": str(project_dir.relative_to(root)),
            "episode_files": episode_paths,
            "quality_report": str(quality_path.relative_to(root)),
            "refinement_trace": str(refinement_path.relative_to(root)),
            "blind_eval_report": str(blind_path.relative_to(root)),
            "episode_count": len(episode_drafts),
            "actual_rendered_scene_count": quality_report["scene_count"],
            "episode_scene_counts": {draft.episode_id: draft.scene_count for draft in episode_drafts},
            "quality_average_after": quality_report["average_after"],
            "quality_average_delta": quality_report["average_delta"],
            "quality_blocker_count_after": quality_report["blocker_count_after"],
            "reveal_leakage_count": quality_report["reveal_leakage_count"],
            "timeline_contradiction_count": quality_report["timeline_contradiction_count"],
            "blind_v1700_margin_over_pure_gpt": blind_report["v1700_margin_over_pure_gpt"],
            "blind_winner": blind_report["winner_source_label"],
            "provider_default_calls": 0,
            "node2_raw_reveal_access_count": 0,
            "commercial_readiness": "release_candidate" if self._passes(quality_report, blind_report, episode_drafts) else "blocked",
            "limitations": [
                "local_first benchmark; no paid external provider API call",
                "candidate evidence pack, not final market release",
                "full 532-scene rendering remains a later scale-up target",
            ],
        }
        manifest_path = project_dir / "commercial_release_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "status": "pass" if manifest["commercial_readiness"] == "release_candidate" else "blocked",
            "commercial_release_manifest": manifest,
            "sample_project_files": episode_paths + [
                str(quality_path.relative_to(root)),
                str(refinement_path.relative_to(root)),
                str(blind_path.relative_to(root)),
                str(manifest_path.relative_to(root)),
            ],
        }

    def _build_episode_drafts(self, composition: Any, traces: list[dict[str, Any]]) -> tuple[EpisodeDraft, EpisodeDraft, EpisodeDraft]:
        chunks = (traces[0:10], traces[10:20], traces[20:30])
        drafts: list[EpisodeDraft] = []
        for index, (episode, chunk) in enumerate(zip(composition.episodes[:3], chunks), start=1):
            macro = next(m for m in composition.macro_plots if m.macro_plot_id == episode.macro_plot_id)
            lines = [
                f"# Generated Episode {index:02d}: {macro.title}",
                "",
                f"- Episode ID: `{episode.episode_id}`",
                f"- Macro Plot: `{episode.macro_plot_id}` — {macro.title}",
                f"- Whole Story Progress: {episode.whole_story_progress}",
                f"- Episode Function: {episode.episode_story_function}",
                "",
                "## Micro Plot Set",
            ]
            for micro in episode.micro_plots:
                lines.extend([
                    f"### {micro.micro_plot_id}",
                    f"- Function: {micro.function_in_episode}",
                    f"- Event Thread: {micro.event_thread}",
                    f"- Character Thread: {micro.character_thread}",
                    f"- Emotional Pressure: {micro.emotional_pressure}",
                    f"- Reveal Policy: {micro.reveal_policy}",
                    "",
                ])
            lines.append("## Rendered Scene Drafts")
            for number, trace in enumerate(chunk, start=1):
                after = trace["after_text"].replace("\n\n", "\n")
                lines.extend([
                    f"### Scene {number:02d} — {trace['scene_id']}",
                    f"- Quality: {trace['before_score']['average']:.2f} → {trace['after_score']['average']:.2f}",
                    f"- Delta: {trace['delta']:.2f}",
                    "",
                    after,
                    "",
                ])
            drafts.append(EpisodeDraft(
                episode_id=episode.episode_id,
                title=macro.title,
                macro_plot_id=episode.macro_plot_id,
                whole_story_progress=episode.whole_story_progress,
                scene_count=len(chunk),
                markdown="\n".join(lines).strip() + "\n",
            ))
        return tuple(drafts)  # type: ignore[return-value]

    def _passes(self, quality_report: dict[str, Any], blind_report: dict[str, Any], drafts: tuple[EpisodeDraft, ...]) -> bool:
        return (
            len(drafts) == 3
            and all(d.scene_count >= 10 for d in drafts)
            and quality_report.get("scene_count", 0) >= 30
            and quality_report.get("average_after", 0.0) >= 8.0
            and quality_report.get("average_delta", 0.0) >= 0.5
            and quality_report.get("blocker_count_after", 1) == 0
            and quality_report.get("reveal_leakage_count", 1) == 0
            and quality_report.get("timeline_contradiction_count", 1) == 0
            and blind_report.get("v1700_margin_over_pure_gpt", 0.0) >= 1.0
            and blind_report.get("winner_source_label") == "v1700_stage81_1_engineered_literary_os"
        )

    def _blind_report_markdown(self, report: dict[str, Any]) -> str:
        lines = [
            "# Stage83 Blind Critic Benchmark Report",
            "",
            f"- Status: {report.get('status')}",
            f"- Winner: {report.get('winner_source_label')}",
            f"- V1700 margin over pure GPT: {report.get('v1700_margin_over_pure_gpt')}",
            f"- Reveal leakage count: {report.get('reveal_leakage_count')}",
            "",
            "## Candidate Scores",
        ]
        for score in report.get("scores", []):
            lines.append(f"- {score['candidate_id']}: {score['average']} / 10")
        lines.extend([
            "",
            "## Interpretation",
            "This is a local-first blind benchmark. It validates the benchmark harness and deterministic V1700 advantage over direct-mode simulation; it does not claim paid external API execution.",
        ])
        return "\n".join(lines) + "\n"


def run_commercial_release_candidate(root: Path | None = None, prompt: str = DEFAULT_PROMPT) -> dict[str, Any]:
    return CommercialLongformReleaseEngine().run(root=root, prompt=prompt)
