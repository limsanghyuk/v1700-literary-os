from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class AgentReviewerProfile:
    agent_id: str
    role: str
    stance: str
    minimum_pass_score: float
    score_weights: dict[str, float]
    red_flag_keywords: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "role": self.role,
            "stance": self.stance,
            "minimum_pass_score": self.minimum_pass_score,
            "score_weights": dict(self.score_weights),
            "red_flag_keywords": list(self.red_flag_keywords),
        }


@dataclass(frozen=True)
class BlindBenchmarkSample:
    blinded_sample_id: str
    visible_order: int
    visible_excerpt: str
    act: str
    reveal_policy: str
    knowledge_mode: str
    source_episode_id: str
    source_scene_id: str
    hidden_origin: str = "stage87_scaleup_evidence"

    def visible_payload(self) -> dict[str, Any]:
        """Payload shown to local reviewer agents without model/stage identity."""
        return {
            "blinded_sample_id": self.blinded_sample_id,
            "visible_order": self.visible_order,
            "visible_excerpt": self.visible_excerpt,
        }

    def to_dict(self, *, include_hidden: bool = True) -> dict[str, Any]:
        payload = self.visible_payload()
        if include_hidden:
            payload.update(
                {
                    "act": self.act,
                    "reveal_policy": self.reveal_policy,
                    "knowledge_mode": self.knowledge_mode,
                    "source_episode_id": self.source_episode_id,
                    "source_scene_id": self.source_scene_id,
                    "hidden_origin": self.hidden_origin,
                }
            )
        return payload


@dataclass(frozen=True)
class AgentAssessment:
    agent_id: str
    blinded_sample_id: str
    axis_scores: dict[str, float]
    weighted_score: float
    verdict: str
    notes: tuple[str, ...]
    red_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "blinded_sample_id": self.blinded_sample_id,
            "axis_scores": dict(self.axis_scores),
            "weighted_score": self.weighted_score,
            "verdict": self.verdict,
            "notes": list(self.notes),
            "red_flags": list(self.red_flags),
        }


@dataclass(frozen=True)
class AgentBenchmarkReport:
    stage: str
    status: str
    sample_count: int
    agent_count: int
    pass_threshold: float
    consensus_score: float
    min_agent_average: float
    min_sample_average: float
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...]
    agents: tuple[AgentReviewerProfile, ...]
    samples: tuple[BlindBenchmarkSample, ...]
    assessments: tuple[AgentAssessment, ...]

    @property
    def assessment_count(self) -> int:
        return len(self.assessments)

    @property
    def agent_averages(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for agent in self.agents:
            scores = [assessment.weighted_score for assessment in self.assessments if assessment.agent_id == agent.agent_id]
            result[agent.agent_id] = round(mean(scores), 2) if scores else 0.0
        return result

    @property
    def sample_averages(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for sample in self.samples:
            scores = [assessment.weighted_score for assessment in self.assessments if assessment.blinded_sample_id == sample.blinded_sample_id]
            result[sample.blinded_sample_id] = round(mean(scores), 2) if scores else 0.0
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "sample_count": self.sample_count,
            "agent_count": self.agent_count,
            "assessment_count": self.assessment_count,
            "pass_threshold": self.pass_threshold,
            "consensus_score": self.consensus_score,
            "min_agent_average": self.min_agent_average,
            "min_sample_average": self.min_sample_average,
            "agent_averages": self.agent_averages,
            "sample_averages": self.sample_averages,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
            "agents": [agent.to_dict() for agent in self.agents],
            "samples": [sample.to_dict(include_hidden=True) for sample in self.samples],
            "visible_blind_samples": [sample.visible_payload() for sample in self.samples],
            "assessments": [assessment.to_dict() for assessment in self.assessments],
        }
