from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode


def build_endurance_episode_plan(episode_count: int = 16) -> tuple[EnduranceEpisode, ...]:
    if episode_count not in {16, 24}:
        raise ValueError("Stage97 supports 16-episode required proof and 24-episode extended proof")
    episodes = []
    for index in range(1, episode_count + 1):
        act = _act(index, episode_count)
        position = index / episode_count
        microplots = 4 + (1 if act in {"jeon", "gyeol"} else 0) + (1 if index in {episode_count // 2, episode_count} else 0)
        scenes = microplots * 3
        reveal = round(0.35 + position * 0.45 + (0.12 if index in {episode_count // 2, episode_count} else 0.0), 3)
        emotional = round(0.45 + position * 0.35, 3)
        conflict = round(0.42 + position * 0.4, 3)
        relationship = round(0.35 + (index % 4) * 0.08, 3)
        motif = round(0.25 + (index % 5) * 0.06, 3)
        exposition = round(max(0.18, 0.58 - position * 0.25), 3)
        agency = round(0.5 + (index % 3) * 0.12 + position * 0.18, 3)
        attention = round(0.48 + (0.18 if index % 4 == 0 else 0.08) + position * 0.16, 3)
        episodes.append(
            EnduranceEpisode(
                episode_id=f"EP{index:02d}",
                act=act,
                position=index,
                microplot_count=microplots,
                scene_count=scenes,
                reveal_load=reveal,
                emotional_load=emotional,
                conflict_load=conflict,
                relationship_load=relationship,
                motif_load=motif,
                exposition_load=exposition,
                agency_load=agency,
                attention_load=attention,
            )
        )
    return tuple(episodes)


def _act(index: int, episode_count: int) -> str:
    ratio = index / episode_count
    if ratio <= 0.25:
        return "gi"
    if ratio <= 0.50:
        return "seung"
    if ratio <= 0.75:
        return "jeon"
    return "gyeol"
