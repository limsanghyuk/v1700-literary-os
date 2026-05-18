from __future__ import annotations

from v1700.longform_endurance.contracts import EnduranceEpisode, FractalPlotUnit


def build_fractal_topology(episodes: tuple[EnduranceEpisode, ...]) -> dict:
    series_id = "series_arc"
    units = [FractalPlotUnit(series_id, "Series", True, True, True, True, True, "", tuple(ep.episode_id for ep in episodes))]
    for episode in episodes:
        micro_ids = tuple(f"{episode.episode_id}_MP{i:02d}" for i in range(1, episode.microplot_count + 1))
        units.append(FractalPlotUnit(episode.episode_id, "Episode", True, True, True, episode.act in {"jeon", "gyeol"}, True, series_id, micro_ids))
        for micro_id in micro_ids:
            scene_ids = tuple(f"{micro_id}_SC{i:02d}" for i in range(1, 4))
            units.append(FractalPlotUnit(micro_id, "MicroPlot", True, True, True, True, True, episode.episode_id, scene_ids))
            for scene_id in scene_ids:
                units.append(FractalPlotUnit(scene_id, "Scene", True, True, True, False, True, micro_id, ()))
    orphan_microplots = [unit.unit_id for unit in units if unit.unit_type == "MicroPlot" and not unit.parent_unit_id]
    episode_coverage = sum(1 for unit in units if unit.unit_type == "Episode" and all([unit.setup, unit.pressure, unit.collision, unit.residue]))
    issues = []
    if orphan_microplots:
        issues.append("orphan_microplot_detected")
    if episode_coverage != len(episodes):
        issues.append("episode_function_coverage_incomplete")
    return {
        "status": "pass" if not issues else "blocked",
        "unit_count": len(units),
        "episode_function_coverage": round(episode_coverage / len(episodes), 3) if episodes else 0,
        "orphan_microplot_count": len(orphan_microplots),
        "units": [unit.to_dict() for unit in units],
        "issues": issues,
    }
