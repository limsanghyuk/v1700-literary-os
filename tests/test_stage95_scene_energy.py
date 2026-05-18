from v1700.narrative_physics.scene_energy import SceneEnergyConservationAudit


def test_stage95_scene_energy_passes_high_quality_scene_set():
    evidence = {"episodes": [{"scenes": [{"quality_score": 8.1}, {"quality_score": 9.0}]}]}

    report = SceneEnergyConservationAudit().audit(evidence).to_dict()
    assert report["status"] == "pass"
    assert report["minimum_energy"] >= 0.81
