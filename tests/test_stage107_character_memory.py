from v1700.longform_production.character_memory_evolution import build_character_memory_evolution


def test_stage107_character_memory_evolution_preserves_agency():
    report = build_character_memory_evolution()
    assert report["status"] == "pass"
    assert report["agency_conservation_status"] == "pass"
    assert report["raw_manuscript_required"] is False
