from v1700.agent_benchmark.agents import build_default_agent_profiles
from v1700.agent_benchmark.harness import AgentBlindBenchmarkHarness, run_stage88_agent_benchmark_smoke
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage88_release_gate import run_stage88_release_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest


def test_stage88_default_agent_panel_has_editor_and_reader_roles():
    agents = build_default_agent_profiles()
    roles = {agent.agent_id for agent in agents}

    assert len(agents) >= 6
    assert "senior_drama_editor_agent" in roles
    assert "platform_serialization_editor_agent" in roles
    assert "continuity_script_editor_agent" in roles
    assert "genre_reader_agent" in roles
    assert "anti_llm_surface_reader_agent" in roles
    assert "skeptical_binge_reader_agent" in roles


def test_stage88_blind_benchmark_builds_complete_agent_assessment_matrix():
    report = AgentBlindBenchmarkHarness().run(episode_count=16, scenes_per_episode=10)

    assert report.status == "pass"
    assert report.agent_count >= 6
    assert report.sample_count >= 16
    assert report.assessment_count == report.agent_count * report.sample_count
    assert report.consensus_score >= 8.0
    assert report.min_agent_average >= 8.0
    assert report.min_sample_average >= 8.0
    assert report.provider_default_calls == 0
    assert report.node2_raw_reveal_access_count == 0
    assert all(sample.blinded_sample_id.startswith("blind_") for sample in report.samples)


def test_stage88_smoke_and_release_gate_preserve_stage87_lineage():
    smoke = run_stage88_agent_benchmark_smoke()
    gate = run_stage88_release_gate()

    assert smoke["status"] == "pass"
    assert gate["status"] == "pass"
    assert gate["checks"]["stage87_release_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_stage88_symbol_trace_manifest_covers_agent_benchmark_branchpoints():
    manifest = build_symbol_to_branchpoint_trace_manifest()
    ids = {entry["branchpoint_id"] for entry in manifest["entries"]}

    assert manifest["status"] == "pass"
    assert "BP_STAGE88_AI_AGENT_EDITOR_PANEL" in ids
    assert "BP_STAGE88_BLIND_SAMPLE_PROTOCOL" in ids
    assert "BP_STAGE88_AGENT_CONSENSUS_GATE" in ids
    assert "BP_STAGE88_PROVIDER_ZERO_AGENT_BENCHMARK" in ids
    assert manifest["coverage"]["P0"]["coverage"] == 1.0


def test_main_release_gate_includes_stage88_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage87_release_gate"]["status"] == "pass"
    assert result["stage88_release_gate"]["status"] == "pass"
