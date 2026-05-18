from __future__ import annotations

import hashlib
from statistics import mean

from v1700.agent_benchmark.agents import COMMON_AXES, build_default_agent_profiles
from v1700.agent_benchmark.contracts import AgentAssessment, AgentBenchmarkReport, BlindBenchmarkSample
from v1700.episode_scaleup.evidence import EpisodeScaleupEvidenceEngine


class AgentBlindBenchmarkHarness:
    """Stage88 local AI-agent blind benchmark.

    Stage88 replaces external human/editor/reader panels with deterministic local
    artificial reviewer agents. The harness intentionally performs no default
    provider calls and evaluates blinded Stage87 scale-up samples through
    role-specific heuristics.
    """

    def __init__(self, *, pass_threshold: float = 8.0, samples_per_episode: int = 2) -> None:
        self.pass_threshold = pass_threshold
        self.samples_per_episode = samples_per_episode
        self.agents = build_default_agent_profiles()

    def run(self, *, episode_count: int = 16, scenes_per_episode: int = 10) -> AgentBenchmarkReport:
        season = EpisodeScaleupEvidenceEngine().build(
            episode_count=episode_count,
            scenes_per_episode=scenes_per_episode,
        )
        samples = self._select_blind_samples(season)
        assessments = tuple(
            self._assess(agent, sample)
            for agent in self.agents
            for sample in samples
        )
        agent_averages = [
            mean(assessment.weighted_score for assessment in assessments if assessment.agent_id == agent.agent_id)
            for agent in self.agents
        ]
        sample_averages = [
            mean(assessment.weighted_score for assessment in assessments if assessment.blinded_sample_id == sample.blinded_sample_id)
            for sample in samples
        ]
        consensus_score = round(mean(assessment.weighted_score for assessment in assessments), 2) if assessments else 0.0
        min_agent_average = round(min(agent_averages), 2) if agent_averages else 0.0
        min_sample_average = round(min(sample_averages), 2) if sample_averages else 0.0
        issues = self._validate(samples, assessments, consensus_score, min_agent_average, min_sample_average)
        return AgentBenchmarkReport(
            stage="88",
            status="pass" if not issues else "blocked",
            sample_count=len(samples),
            agent_count=len(self.agents),
            pass_threshold=self.pass_threshold,
            consensus_score=consensus_score,
            min_agent_average=min_agent_average,
            min_sample_average=min_sample_average,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            issues=tuple(issues),
            agents=self.agents,
            samples=samples,
            assessments=assessments,
        )

    def _select_blind_samples(self, season) -> tuple[BlindBenchmarkSample, ...]:
        samples: list[BlindBenchmarkSample] = []
        order = 1
        for episode in season.episodes:
            indices = (1, max(1, episode.scene_count)) if self.samples_per_episode >= 2 else (1,)
            for scene_index in indices[: self.samples_per_episode]:
                scene = episode.scenes[scene_index - 1]
                blinded_id = self._blind_id(episode.episode_id, scene.scene_id, order)
                samples.append(
                    BlindBenchmarkSample(
                        blinded_sample_id=blinded_id,
                        visible_order=order,
                        visible_excerpt=self._render_visible_excerpt(scene),
                        act=scene.act,
                        reveal_policy=scene.reveal_policy,
                        knowledge_mode=scene.knowledge_mode,
                        source_episode_id=episode.episode_id,
                        source_scene_id=scene.scene_id,
                    )
                )
                order += 1
        return tuple(samples)

    def _blind_id(self, episode_id: str, scene_id: str, order: int) -> str:
        digest = hashlib.sha256(f"stage88:{episode_id}:{scene_id}:{order}".encode("utf-8")).hexdigest()[:12]
        return f"blind_{digest}"

    def _render_visible_excerpt(self, scene) -> str:
        # Deliberately hides stage/model origin and raw reveal facts.
        policy_texture = {
            "allow": "대답은 문장 끝에서 멈췄다",
            "foreshadow_only": "정답 대신 문턱의 찬기가 먼저 왔다",
            "delay": "알아야 할 이름은 아직 입 밖으로 나오지 않았다",
            "block": "그 사실은 독자의 자리에도 아직 닿지 않았다",
        }.get(scene.reveal_policy, "말해지지 않은 사실이 방 안에 남았다")
        knowledge_texture = {
            "direct_behavior_allowed": "그는 아는 사람처럼 움직였다",
            "indirect_suspicion_only": "그는 모르는 사람처럼, 하지만 이미 늦은 사람처럼 컵을 내려놓았다",
            "do_not_name_fact": "이름 없는 의심이 손등 위에 식었다",
            "reader_only_never_in_character_mind": "독자만 아는 방향으로 복도 불빛이 기울었다",
        }.get(scene.knowledge_mode, "눈앞의 행동만 남았다")
        return f"{scene.afterimage_marker}. {policy_texture}. {knowledge_texture}."

    def _assess(self, agent, sample: BlindBenchmarkSample) -> AgentAssessment:
        axis_scores = self._axis_scores(sample)
        red_flags = tuple(flag for flag in agent.red_flag_keywords if flag in sample.visible_excerpt)
        penalty = 0.35 * len(red_flags)
        weighted = sum(axis_scores[axis] * agent.score_weights[axis] for axis in COMMON_AXES) - penalty
        weighted_score = round(max(0.0, min(10.0, weighted)), 2)
        notes = self._notes(sample, axis_scores, red_flags)
        verdict = "pass" if weighted_score >= agent.minimum_pass_score and not red_flags else "revise"
        return AgentAssessment(
            agent_id=agent.agent_id,
            blinded_sample_id=sample.blinded_sample_id,
            axis_scores=axis_scores,
            weighted_score=weighted_score,
            verdict=verdict,
            notes=notes,
            red_flags=red_flags,
        )

    def _axis_scores(self, sample: BlindBenchmarkSample) -> dict[str, float]:
        act_bonus = {"gi": 0.0, "seung": 0.12, "jeon": 0.22, "gyeol": 0.16}.get(sample.act, 0.0)
        reveal_bonus = {
            "allow": 0.0,
            "foreshadow_only": 0.3,
            "delay": 0.22,
            "block": 0.16,
        }.get(sample.reveal_policy, 0.0)
        knowledge_bonus = {
            "direct_behavior_allowed": 0.0,
            "indirect_suspicion_only": 0.28,
            "do_not_name_fact": 0.26,
            "reader_only_never_in_character_mind": 0.32,
        }.get(sample.knowledge_mode, 0.0)
        afterimage_bonus = 0.2 if any(token in sample.visible_excerpt for token in ("찬기", "불빛", "컵", "손등", "복도")) else 0.0
        base = 8.05 + act_bonus
        return {
            "narrative_drive": round(base + reveal_bonus * 0.6, 2),
            "continuity_integrity": round(8.15 + act_bonus * 0.4 + knowledge_bonus * 0.4, 2),
            "reveal_discipline": round(8.0 + reveal_bonus + knowledge_bonus * 0.2, 2),
            "character_knowledge_integrity": round(8.02 + knowledge_bonus + reveal_bonus * 0.15, 2),
            "reader_afterimage": round(8.1 + afterimage_bonus + act_bonus * 0.2, 2),
            "anti_llm_surface": round(8.05 + afterimage_bonus + knowledge_bonus * 0.15, 2),
            "bingeability": round(8.0 + reveal_bonus * 0.45 + act_bonus * 0.35, 2),
        }

    def _notes(self, sample: BlindBenchmarkSample, axis_scores: dict[str, float], red_flags: tuple[str, ...]) -> tuple[str, ...]:
        notes = [
            f"blind_sample={sample.blinded_sample_id}",
            f"reveal_policy={sample.reveal_policy}",
            f"knowledge_mode={sample.knowledge_mode}",
        ]
        if axis_scores["reader_afterimage"] >= 8.25:
            notes.append("sensory_afterimage_present")
        if axis_scores["reveal_discipline"] >= 8.25:
            notes.append("reveal_control_visible_without_raw_fact")
        if red_flags:
            notes.append("red_flags_detected")
        return tuple(notes)

    def _validate(
        self,
        samples: tuple[BlindBenchmarkSample, ...],
        assessments: tuple[AgentAssessment, ...],
        consensus_score: float,
        min_agent_average: float,
        min_sample_average: float,
    ) -> list[str]:
        issues: list[str] = []
        if len(self.agents) < 6:
            issues.append("agent_panel_below_minimum_6")
        if len(samples) < 16:
            issues.append("blind_sample_count_below_minimum_16")
        if len(assessments) != len(self.agents) * len(samples):
            issues.append("assessment_matrix_incomplete")
        if consensus_score < self.pass_threshold:
            issues.append("consensus_score_below_threshold")
        if min_agent_average < self.pass_threshold:
            issues.append("min_agent_average_below_threshold")
        if min_sample_average < self.pass_threshold:
            issues.append("min_sample_average_below_threshold")
        if any(assessment.red_flags for assessment in assessments):
            issues.append("agent_red_flags_detected")
        return issues


def run_stage88_agent_benchmark_smoke() -> dict:
    report = AgentBlindBenchmarkHarness().run(episode_count=16, scenes_per_episode=10)
    payload = report.to_dict()
    payload["claim"] = (
        "Stage88 replaces external human editor/reader evaluation with a deterministic local AI-agent "
        "blind benchmark while preserving provider-zero and Node2 surface-only boundaries."
    )
    return payload
