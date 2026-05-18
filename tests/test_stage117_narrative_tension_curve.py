from v1700.nie.arc import NarrativeTensionCurve, build_stage117_tension_curve_report
from v1700.nie.arc.contracts import SceneTensionPoint
from v1700.stage117.orchestrator import run_stage117
from v1700.gates.stage117_release_gate import run_stage117_release_gate


def test_ideal_curve_is_bounded() -> None:
    curve = NarrativeTensionCurve()
    values = [curve.ideal(i / 20) for i in range(21)]
    assert all(0.0 <= value <= 1.0 for value in values)
    assert len(set(values)) > 5


def test_tension_and_coverage_loss() -> None:
    curve = NarrativeTensionCurve()
    scenes = [
        SceneTensionPoint("s1", 0.05, curve.ideal(0.05), 1),
        SceneTensionPoint("s2", 0.16, curve.ideal(0.16), 1),
        SceneTensionPoint("s3", 0.30, curve.ideal(0.30), 2),
        SceneTensionPoint("s4", 0.42, curve.ideal(0.42), 2),
        SceneTensionPoint("s5", 0.56, curve.ideal(0.56), 3),
        SceneTensionPoint("s6", 0.69, curve.ideal(0.69), 3),
        SceneTensionPoint("s7", 0.82, curve.ideal(0.82), 4),
        SceneTensionPoint("s8", 0.95, curve.ideal(0.95), 4),
    ]
    assert curve.tension_loss(scenes) == 0.0
    assert curve.coverage_loss(scenes) == 0.0
    assert curve.final_loss(scenes) == 0.0


def test_coverage_loss_blocks_missing_act() -> None:
    curve = NarrativeTensionCurve()
    scenes = [SceneTensionPoint("s1", 0.05, 0.4, 1), SceneTensionPoint("s2", 0.30, 0.5, 2)]
    assert curve.coverage_loss(scenes) > 0
    assert curve.evaluate(scenes).status == "BLOCK"


def test_stage117_report_and_gate_pass(tmp_path) -> None:
    report = build_stage117_tension_curve_report()
    assert report["status"] == "pass"
    assert report["loss"]["coverage_loss"] == 0.0
    assert report["loss"]["final_loss"] < 0.10


def test_stage117_orchestrator_and_gate_on_repo_root() -> None:
    stage = run_stage117()
    assert stage["status"] == "pass"
    gate = run_stage117_release_gate()
    assert gate["status"] == "pass"
    assert gate["checks"]["narrative_tension_curve_contract_pass"]["status"] == "pass"
