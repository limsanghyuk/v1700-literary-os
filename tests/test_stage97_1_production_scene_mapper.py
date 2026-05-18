from pathlib import Path

from v1700.longform_adversarial.production_scene_mapper import build_production_scene_mapping

ROOT = Path(__file__).resolve().parents[1]


def test_structural_scene_to_production_scene_mapping_preserves_density():
    report = build_production_scene_mapping(ROOT)
    assert report["status"] == "pass"
    assert report["episode_count"] == 16
    assert report["total_production_scene_count_estimate"] >= report["total_structural_scene_count"]
    assert all(item["major_sequence_count"] >= 4 for item in report["mappings"])
