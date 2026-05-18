from pathlib import Path

from v1700.stage101.absorption_matrix import run_stage101_absorption_matrix
from v1700.stage101.source_probe import run_stage101_v430_source_probe

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_absorption_matrix_allows_only_traced_adapt_or_defer():
    source = run_stage101_v430_source_probe(ROOT)
    matrix = run_stage101_absorption_matrix(ROOT, source)
    assert matrix["status"] == "pass"
    assert matrix["v430_untraced_merge"] is False
    assert {item["proposed_action"] for item in matrix["candidates"]} <= {"ADAPT", "DEFER"}
    assert all(item["required_branchpoints"] and item["required_tests"] for item in matrix["candidates"])

