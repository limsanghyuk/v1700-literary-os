from v1700.episode_scaleup.evidence import EpisodeScaleupEvidenceEngine, run_stage87_episode_scaleup_smoke
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage87_release_gate import run_stage87_release_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest


def test_stage87_builds_eight_episode_scaleup_evidence():
    evidence = EpisodeScaleupEvidenceEngine().build(episode_count=8, scenes_per_episode=10)

    assert evidence.status == "pass"
    assert evidence.episode_count == 8
    assert evidence.total_scene_count == 80
    assert set(evidence.act_coverage) == {"gi", "seung", "jeon", "gyeol"}
    assert evidence.edge_counts["causal"] >= 7
    assert evidence.min_quality_score >= 8.0
    assert evidence.provider_default_calls == 0
    assert evidence.node2_raw_reveal_access_count == 0


def test_stage87_builds_sixteen_episode_scaleup_evidence_with_reveal_and_knowledge_locks():
    evidence = EpisodeScaleupEvidenceEngine().build(episode_count=16, scenes_per_episode=10)

    assert evidence.status == "pass"
    assert evidence.episode_count == 16
    assert evidence.total_scene_count == 160
    assert evidence.blocked_direct_reveal_count > 0
    assert evidence.knowledge_constraint_count > 0
    assert evidence.edge_counts["foreshadow"] >= 4
    assert evidence.edge_counts["callback"] >= 4
    assert all(scene.surface_only for episode in evidence.episodes for scene in episode.scenes)


def test_stage87_smoke_and_release_gate_preserve_prior_lineage():
    smoke = run_stage87_episode_scaleup_smoke()
    gate = run_stage87_release_gate()

    assert smoke["status"] == "pass"
    assert gate["status"] == "pass"
    assert gate["checks"]["stage86_release_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_stage87_symbol_trace_manifest_covers_new_p0_branchpoints():
    manifest = build_symbol_to_branchpoint_trace_manifest()
    ids = {entry["branchpoint_id"] for entry in manifest["entries"]}

    assert manifest["status"] == "pass"
    assert "BP_STAGE87_EIGHT_EPISODE_SCALEUP" in ids
    assert "BP_STAGE87_SIXTEEN_EPISODE_SCALEUP" in ids
    assert "BP_STAGE87_REVEAL_KNOWLEDGE_SCALE_LOCK" in ids
    assert manifest["coverage"]["P0"]["coverage"] == 1.0


def test_main_release_gate_includes_stage87_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage87_release_gate"]["status"] == "pass"
