from __future__ import annotations

from pathlib import Path

from v1700.gates.stage123_release_gate import run_stage123_release_gate
from v1700.nie.asd import Gate28, StoryDoctorOrchestrator, AutoRepairExecutor
from v1700.stage123.fixtures import ASD_FIXTURE_GRAPH, BLOCKING_ASD_GRAPH
from v1700.stage123.orchestrator import run_stage123

ROOT = Path(__file__).resolve().parents[1]


def test_stage123_orchestrator_passes_and_keeps_gate28_secondary():
    result = run_stage123(ROOT)
    assert result["status"] == "pass"
    assert result["absorption_policy"]["gate28_authority_mode"] == "secondary_quality_gate"
    assert result["absorption_policy"]["gate28_primary_authority_enabled"] is False
    assert result["absorption_policy"]["graph_mutation_enabled"] is False
    assert result["absorption_policy"]["direct_v545_merge_performed"] is False


def test_story_doctor_priority_formula_matches_v545_concept():
    report = StoryDoctorOrchestrator().diagnose(ASD_FIXTURE_GRAPH)
    assert report.status == "pass"
    assert report.provider_calls == 0
    assert report.mutation_allowed is False
    assert report.recommendations
    first = report.recommendations[0]
    assert first.priority_score == round(min(1.0, first.severity * (1 + 1.5 * first.blast_ratio)), 6)


def test_gate28_passes_fixture_and_blocks_negative_case():
    doctor = StoryDoctorOrchestrator()
    good = Gate28().evaluate(doctor.diagnose(ASD_FIXTURE_GRAPH))
    bad = Gate28().evaluate(doctor.diagnose(BLOCKING_ASD_GRAPH))
    assert good.status == "pass"
    assert good.authority_mode == "secondary_quality_gate"
    assert bad.status == "blocked"
    assert bad.failed_gates


def test_auto_repair_executor_is_dry_run_only():
    report = StoryDoctorOrchestrator().diagnose(ASD_FIXTURE_GRAPH)
    execution = AutoRepairExecutor().execute_batch(report.recommendations, dry_run=True)
    assert execution.status == "pass"
    assert execution.mutation_count == 0
    assert execution.dry_run == execution.total


def test_stage123_release_gate_passes():
    result = run_stage123_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["checks"]["gate28_secondary_quality_gate"]["status"] == "pass"
    assert result["checks"]["auto_repair_dry_run_only"]["status"] == "pass"
    assert result["story_doctor_llm_call_count"] == 0
