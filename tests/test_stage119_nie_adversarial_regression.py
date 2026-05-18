from v1700.nie.adversarial import build_stage119_cases, evaluate_cases, build_stage119_adversarial_report
from v1700.stage119.orchestrator import run_stage119
from v1700.gates.stage119_release_gate import run_stage119_release_gate


def test_stage119_cases_include_normal_and_12_block_cases() -> None:
    cases = build_stage119_cases()
    assert sum(1 for case in cases if case.expected_status == "PASS") == 1
    assert sum(1 for case in cases if case.expected_status == "BLOCK") >= 12
    assert all(case.expected_block_reason for case in cases if case.expected_status == "BLOCK")


def test_stage119_adversarial_results_match_expectations() -> None:
    results = evaluate_cases(build_stage119_cases())
    assert all(result.matched_expectation for result in results)
    assert not [result for result in results if result.expected_status == "BLOCK" and result.actual_status != "BLOCK"]


def test_stage119_report_and_gate_pass_on_repo_root() -> None:
    report = build_stage119_adversarial_report()
    assert report["status"] == "pass"
    assert report["unexpected_pass_count"] == 0
    stage = run_stage119()
    assert stage["status"] == "pass"
    gate = run_stage119_release_gate()
    assert gate["status"] == "pass"
    assert gate["checks"]["adversarial_minimum_case_count_pass"]["status"] == "pass"
    assert gate["checks"]["failure_evidence_reproducibility_pass"]["status"] == "pass"
