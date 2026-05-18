from pathlib import Path

from v1700.gates.longform_execution_gate import run_longform_execution_gate
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage74_release_gate import run_stage74_release_gate
from v1700.longform import LongformExecutionEngine, run_longform_execution_smoke

ROOT = Path(__file__).resolve().parents[1]


def test_stage74_longform_engine_generates_three_episode_plan_and_rendered_scene():
    report = LongformExecutionEngine().execute("비밀을 숨긴 조력자와 사라진 증거")
    data = report.to_dict()

    assert data["status"] == "pass"
    assert len(data["plan"]["episodes"]) == 3
    assert len(data["scenes"]) == 3
    assert data["rendered"]
    assert data["drse"]["scores"]
    assert data["emotional_momentum"]["intensity"] > 0
    assert data["mise_en_scene"]["sensory_directives"]
    assert data["reveal_budget"]["leakage"] == []
    assert data["provider_default_calls"] == 0
    assert data["node2_raw_reveal_access_count"] == 0


def test_stage74_gates_and_main_release_gate_pass():
    smoke = run_longform_execution_smoke()
    longform_gate = run_longform_execution_gate(ROOT)
    stage74 = run_stage74_release_gate(ROOT)
    main = run_release_gate()

    assert smoke["status"] == "pass"
    assert longform_gate["status"] == "pass"
    assert stage74["status"] == "pass"
    assert main["status"] == "pass"
    assert main["stage73_1_release_gate"]["status"] == "pass"
    assert main["stage74_release_gate"]["status"] == "pass"
