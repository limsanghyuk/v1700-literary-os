from __future__ import annotations
from .contracts import EditorialReviewer, ReviewPacket, EditorialScorecard

_BASE_BY_MODE = {
    "PROSE": {"literary_merit": 8.8, "voice_integrity": 8.6, "originality": 8.3, "surface_polish": 8.4},
    "SCENARIO": {"scene_beat": 8.7, "dialogue_subtext": 8.4, "visual_clarity": 8.8, "production_feasibility": 8.2},
    "LONGFORM_STRUCTURE": {"continuity": 9.1, "payoff_coherence": 8.9, "character_memory": 8.8, "attention_curve": 8.6},
    "PRODUCTION_READINESS": {"workspace_readiness": 8.7, "export_loop": 8.5, "review_queue": 8.8, "privacy_posture": 9.5},
}

def score_packet(reviewer: EditorialReviewer, packet: ReviewPacket) -> EditorialScorecard:
    breakdown = dict(_BASE_BY_MODE[packet.mode])
    role_bonus = {
        "LITERARY_CRITIC": {"PROSE": 0.25},
        "DRAMATURG": {"SCENARIO": 0.15, "LONGFORM_STRUCTURE": 0.10},
        "MARKET_EDITOR": {"PRODUCTION_READINESS": 0.10},
        "GENRE_EDITOR": {"SCENARIO": 0.10},
        "CONTINUITY_AUDITOR": {"LONGFORM_STRUCTURE": 0.25},
        "SCENARIO_PRODUCER": {"SCENARIO": 0.25},
    }.get(reviewer.role, {}).get(packet.mode, 0.0)
    average = sum(breakdown.values()) / len(breakdown)
    weighted = min(9.9, round((average + role_bonus) * min(1.05, reviewer.weight), 2))
    relevance = "WARN" if weighted < 8.0 else "INFO"
    if packet.contains_raw_manuscript:
        relevance = "BLOCK"
    return EditorialScorecard(
        scorecard_id=f"score_{reviewer.reviewer_id}_{packet.packet_id}",
        reviewer_id=reviewer.reviewer_id,
        packet_id=packet.packet_id,
        mode=packet.mode,
        score_total=weighted,
        score_breakdown=breakdown,
        release_relevance=relevance,
        notes=[f"{reviewer.role} reviewed {packet.mode} through feature-only packet"],
    )

def build_scorecards(reviewers: list[EditorialReviewer], packets: list[ReviewPacket]) -> list[EditorialScorecard]:
    return [score_packet(r, p) for r in reviewers for p in packets]
