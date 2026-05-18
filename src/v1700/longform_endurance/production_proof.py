from __future__ import annotations

from v1700.longform_endurance.agency_conservation import evaluate_agency_conservation
from v1700.longform_endurance.attention_economy import evaluate_attention_economy
from v1700.longform_endurance.dialogue_pragmatics import evaluate_dialogue_pragmatics
from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.fractal_topology import build_fractal_topology
from v1700.longform_endurance.load_balancing import evaluate_dramatic_load
from v1700.longform_endurance.payoff_debt import build_payoff_debt_ledger
from v1700.longform_endurance.scene_necessity import evaluate_scene_necessity
from v1700.longform_endurance.voice_manifold import evaluate_voice_manifold


def build_longform_production_proof(episode_count: int = 16) -> dict:
    episodes = build_endurance_episode_plan(episode_count)
    topology = build_fractal_topology(episodes)
    load = evaluate_dramatic_load(episodes)
    agency = evaluate_agency_conservation(episodes)
    payoff = build_payoff_debt_ledger(episodes)
    scene = evaluate_scene_necessity(episodes)
    dialogue = evaluate_dialogue_pragmatics(episodes)
    voice = evaluate_voice_manifold(episodes)
    attention = evaluate_attention_economy(episodes)
    checks = {
        "fractal_topology": topology,
        "dramatic_load_balancing": load,
        "agency_conservation": agency,
        "payoff_debt_ledger": payoff,
        "scene_necessity": scene,
        "dialogue_pragmatics": dialogue,
        "voice_manifold": voice,
        "attention_economy": attention,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    scene_count = sum(episode.scene_count for episode in episodes)
    microplot_count = sum(episode.microplot_count for episode in episodes)
    if episode_count == 16 and scene_count < 160:
        issues.append("sixteen_episode_scene_count_below_160")
    return {
        "status": "pass" if not issues else "blocked",
        "episode_count": episode_count,
        "microplot_count": microplot_count,
        "scene_count_estimate": scene_count,
        "episodes": [episode.to_dict() for episode in episodes],
        "checks": checks,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "issues": issues,
    }
