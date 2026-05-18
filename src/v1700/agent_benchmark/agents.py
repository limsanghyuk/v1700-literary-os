from __future__ import annotations

from v1700.agent_benchmark.contracts import AgentReviewerProfile

COMMON_AXES = (
    "narrative_drive",
    "continuity_integrity",
    "reveal_discipline",
    "character_knowledge_integrity",
    "reader_afterimage",
    "anti_llm_surface",
    "bingeability",
)


def _weights(**overrides: float) -> dict[str, float]:
    base = {
        "narrative_drive": 1.0,
        "continuity_integrity": 1.0,
        "reveal_discipline": 1.0,
        "character_knowledge_integrity": 1.0,
        "reader_afterimage": 1.0,
        "anti_llm_surface": 1.0,
        "bingeability": 1.0,
    }
    base.update(overrides)
    total = sum(base.values())
    return {axis: round(value / total, 4) for axis, value in base.items()}


def build_default_agent_profiles() -> tuple[AgentReviewerProfile, ...]:
    """Return deterministic local AI reviewer agents replacing external humans.

    These are not external LLM calls. They are rule-driven artificial reviewer
    agents that emulate distinct editorial/reader stances while keeping provider
    default calls at zero.
    """

    return (
        AgentReviewerProfile(
            agent_id="senior_drama_editor_agent",
            role="Senior Korean drama editor",
            stance="Checks dramatic escalation, episode rhythm, and scene afterimage.",
            minimum_pass_score=8.0,
            score_weights=_weights(narrative_drive=1.4, continuity_integrity=1.2, reader_afterimage=1.2),
            red_flag_keywords=("설명했다", "복잡한 감정", "갑자기"),
        ),
        AgentReviewerProfile(
            agent_id="platform_serialization_editor_agent",
            role="Commercial serialization platform editor",
            stance="Checks hook density, bingeability, and episode-to-episode retention.",
            minimum_pass_score=8.0,
            score_weights=_weights(bingeability=1.6, narrative_drive=1.25, reveal_discipline=1.1),
            red_flag_keywords=("늘어졌다", "정체", "정보 과다"),
        ),
        AgentReviewerProfile(
            agent_id="continuity_script_editor_agent",
            role="Continuity and script logic editor",
            stance="Checks causal anchors, continuity, and reveal-budget consistency.",
            minimum_pass_score=8.0,
            score_weights=_weights(continuity_integrity=1.65, reveal_discipline=1.3, character_knowledge_integrity=1.2),
            red_flag_keywords=("모순", "잊었다", "설정 붕괴"),
        ),
        AgentReviewerProfile(
            agent_id="genre_reader_agent",
            role="Korean longform genre reader",
            stance="Checks emotional readability, serial momentum, and curiosity gap.",
            minimum_pass_score=8.0,
            score_weights=_weights(reader_afterimage=1.35, bingeability=1.35, narrative_drive=1.15),
            red_flag_keywords=("밋밋", "인물 없음", "다음 화가 안 궁금"),
        ),
        AgentReviewerProfile(
            agent_id="anti_llm_surface_reader_agent",
            role="AI-scent and prose surface detector",
            stance="Penalizes abstract emotion, generic summary, and non-sensory prose.",
            minimum_pass_score=8.0,
            score_weights=_weights(anti_llm_surface=1.8, reader_afterimage=1.2, character_knowledge_integrity=1.1),
            red_flag_keywords=("복잡한 감정", "마음이 복잡", "분위기가 묘했다", "중요한 순간"),
        ),
        AgentReviewerProfile(
            agent_id="skeptical_binge_reader_agent",
            role="Skeptical binge reader",
            stance="Scores only what would keep a tired reader moving to the next episode.",
            minimum_pass_score=8.0,
            score_weights=_weights(bingeability=1.8, narrative_drive=1.2, reader_afterimage=1.1),
            red_flag_keywords=("예상 가능", "흥미 없음", "설명"),
        ),
    )
