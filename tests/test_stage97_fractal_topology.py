from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.fractal_topology import build_fractal_topology


def test_stage97_fractal_topology_covers_all_episodes_without_orphans():
    report = build_fractal_topology(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["episode_function_coverage"] == 1.0
    assert report["orphan_microplot_count"] == 0
