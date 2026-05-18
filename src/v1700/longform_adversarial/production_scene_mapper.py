from __future__ import annotations

from pathlib import Path

from v1700.longform_adversarial.contracts import ProductionSceneMapping
from v1700.longform_endurance.endurance_orchestrator import run_stage97_longform_endurance


def build_production_scene_mapping(root: Path | None = None, runtime_minutes: int = 60) -> dict:
    root = root or Path.cwd()
    endurance = run_stage97_longform_endurance(root)
    episodes = endurance["required_16_episode_proof"]["episodes"]
    mappings = []
    issues = []
    for episode in episodes:
        structural_scene_count = int(episode["scene_count"])
        microplot_count = int(episode["microplot_count"])
        production_scene_count = structural_scene_count * 4
        major_sequence_count = min(6, max(4, microplot_count))
        beat_count = production_scene_count * 3
        if production_scene_count < 45:
            density = "WARN"
            issues.append(f"{episode['episode_id']}_production_scene_density_low")
        elif production_scene_count > 80:
            density = "WARN"
            issues.append(f"{episode['episode_id']}_production_scene_density_high")
        else:
            density = "PASS"
        mappings.append(
            ProductionSceneMapping(
                episode_id=episode["episode_id"],
                structural_scene_count=structural_scene_count,
                production_scene_count_estimate=production_scene_count,
                major_sequence_count=major_sequence_count,
                microplot_count=microplot_count,
                beat_count_estimate=beat_count,
                runtime_minutes=runtime_minutes,
                density_status=density,
            )
        )
    blocking = [item for item in mappings if item.density_status == "BLOCK"]
    return {
        "status": "pass" if not blocking else "blocked",
        "mapping_policy": "structural_scene_to_production_scene_estimate",
        "episode_count": len(mappings),
        "total_structural_scene_count": sum(item.structural_scene_count for item in mappings),
        "total_production_scene_count_estimate": sum(item.production_scene_count_estimate for item in mappings),
        "mappings": [item.to_dict() for item in mappings],
        "warnings": issues,
        "issues": [item.episode_id for item in blocking],
    }
