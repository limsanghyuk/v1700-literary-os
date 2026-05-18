from __future__ import annotations

from v1700.manuscript_learning.contracts import SceneFeature


def mine_scene_patterns(features: tuple[SceneFeature, ...]) -> dict:
    high_energy = [item.scene_id for item in features if item.scene_energy_output >= 0.8]
    reveal_scenes = [item.scene_id for item in features if item.reveal_event_count]
    hooks = [item.scene_id for item in features if item.curiosity_hook_count]
    belief_shifts = [item.scene_id for item in features if item.belief_state_change_count]
    return {
        "high_energy_scene_pattern": high_energy[:12],
        "successful_reveal_pattern": reveal_scenes[:12],
        "episode_ending_hook_pattern": hooks[:12],
        "character_belief_shift_pattern": belief_shifts[:12],
        "fatigue_pattern": [],
        "premature_reveal_pattern": [],
        "low_energy_dead_scene_pattern": [],
        "motif_payoff_pattern": [item.scene_id for item in features if item.callback_count][:12],
    }
